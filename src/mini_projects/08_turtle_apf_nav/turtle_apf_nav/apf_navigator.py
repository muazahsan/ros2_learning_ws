import math

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from geometry_msgs.msg import Point, Twist
from std_msgs.msg import Bool, String
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

from turtle_apf_nav.obstacle_manager import OBSTACLES


NEON_PALETTE = [
    (0, 255, 255),    # Cyan
    (57, 255, 20),    # Neon Green
    (255, 0, 255),    # Magenta
    (255, 200, 0),    # Gold
]

GOAL_TOLERANCE = 0.55


def wrap_angle(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


class APFNavigator(Node):
    """Autonomous obstacle-avoiding navigator using Artificial Potential Fields."""

    def __init__(self):
        super().__init__('apf_navigator')

        # Live-tunable ROS 2 parameters!
        self.declare_parameter('max_speed', 2.6)
        self.declare_parameter('attraction_gain', 1.8)
        self.declare_parameter('repulsion_gain', 3.5)
        self.declare_parameter('repulsion_radius', 2.1)

        self.max_speed = self.get_parameter('max_speed').value
        self.attraction_gain = self.get_parameter('attraction_gain').value
        self.repulsion_gain = self.get_parameter('repulsion_gain').value
        self.repulsion_radius = self.get_parameter('repulsion_radius').value

        # Allow live updates via `ros2 param set /apf_navigator <param> <value>`
        self.add_on_set_parameters_callback(self.on_param_change)

        self.pose = None
        self.goal = None
        self.color_idx = 0
        self.goal_cooldown = 0

        self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.create_subscription(Point, '/apf/goal', self.goal_callback, 10)

        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.reached_pub = self.create_publisher(Bool, '/apf/goal_reached', 10)
        self.status_pub = self.create_publisher(String, '/apf/status', 10)
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')

        # 20 Hz APF navigation loop + 2 Hz telemetry status
        self.create_timer(0.05, self.control_loop)
        self.create_timer(0.5, self.publish_status)

        self.get_logger().info(
            'APF Navigator started! Tune live with: '
            'ros2 param set /apf_navigator repulsion_radius 3.0'
        )

    def on_param_change(self, params):
        for p in params:
            if p.name == 'max_speed' and p.value > 0.1:
                self.max_speed = float(p.value)
            elif p.name == 'attraction_gain' and p.value > 0.0:
                self.attraction_gain = float(p.value)
            elif p.name == 'repulsion_gain' and p.value >= 0.0:
                self.repulsion_gain = float(p.value)
            elif p.name == 'repulsion_radius' and p.value > 0.2:
                self.repulsion_radius = float(p.value)
            else:
                return SetParametersResult(successful=False, reason='Invalid parameter value')
            self.get_logger().info(f'Updated parameter {p.name} = {p.value}')
        return SetParametersResult(successful=True)

    def pose_callback(self, msg: Pose):
        self.pose = msg

    def goal_callback(self, msg: Point):
        self.goal = (msg.x, msg.y)

    def cycle_pen_color(self):
        if not self.pen_client.service_is_ready():
            return
        self.color_idx = (self.color_idx + 1) % len(NEON_PALETTE)
        r, g, b = NEON_PALETTE[self.color_idx]
        req = SetPen.Request()
        req.r, req.g, req.b, req.width, req.off = r, g, b, 3, 0
        self.pen_client.call_async(req)

    def compute_apf_vector(self):
        """Combine goal attraction + obstacle repulsion (with tangential swirl) + walls."""
        gx, gy = self.goal
        dx_g = gx - self.pose.x
        dy_g = gy - self.pose.y
        dist_goal = math.hypot(dx_g, dy_g)

        # 1. Attractive force pulling toward the goal
        fx = self.attraction_gain * (dx_g / max(dist_goal, 0.01))
        fy = self.attraction_gain * (dy_g / max(dist_goal, 0.01))

        # 2. Repulsive force pushing away from every obstacle within repulsion_radius
        nearest_obs = 99.0
        for _, ox, oy in OBSTACLES:
            rx = self.pose.x - ox
            ry = self.pose.y - oy
            dist_obs = math.hypot(rx, ry)
            nearest_obs = min(nearest_obs, dist_obs)

            if 0.05 < dist_obs < self.repulsion_radius:
                mag = (
                    self.repulsion_gain
                    * (1.0 / dist_obs - 1.0 / self.repulsion_radius)
                    / (dist_obs * dist_obs)
                )
                mag = min(mag, 8.0)

                ux = rx / dist_obs
                uy = ry / dist_obs

                # Add 25% tangential swirl (-uy, ux) to prevent head-on local-minimum traps
                fx += mag * (ux - 0.25 * uy)
                fy += mag * (uy + 0.25 * ux)

        # 3. Gentle arena wall boundary repulsion
        if self.pose.x < 0.9:
            fx += 2.5 * (0.9 - self.pose.x)
        elif self.pose.x > 10.1:
            fx -= 2.5 * (self.pose.x - 10.1)
        if self.pose.y < 0.9:
            fy += 2.5 * (0.9 - self.pose.y)
        elif self.pose.y > 10.1:
            fy -= 2.5 * (self.pose.y - 10.1)

        return fx, fy, dist_goal, nearest_obs

    def control_loop(self):
        if self.pose is None or self.goal is None:
            return

        if self.goal_cooldown > 0:
            self.goal_cooldown -= 1

        fx, fy, dist_goal, _ = self.compute_apf_vector()

        # Check if goal reached
        if dist_goal < GOAL_TOLERANCE and self.goal_cooldown == 0:
            self.cmd_pub.publish(Twist())
            self.reached_pub.publish(Bool(data=True))
            self.cycle_pen_color()
            self.goal_cooldown = 15  # Wait 0.75s for new goal update
            return

        desired_angle = math.atan2(fy, fx)
        angle_error = wrap_angle(desired_angle - self.pose.theta)

        cmd = Twist()
        cmd.angular.z = max(-5.5, min(5.5, 5.5 * angle_error))
        alignment = max(0.2, math.cos(angle_error))
        cmd.linear.x = min(self.max_speed, max(0.4, self.max_speed * alignment))

        self.cmd_pub.publish(cmd)

    def publish_status(self):
        if self.pose is None or self.goal is None:
            return
        _, _, dist_goal, nearest_obs = self.compute_apf_vector()
        msg = String()
        msg.data = (
            f'dist_to_goal={dist_goal:.2f} | nearest_obstacle={nearest_obs:.2f} | '
            f'repulsion_radius={self.repulsion_radius:.2f} | max_speed={self.max_speed:.2f}'
        )
        self.status_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = APFNavigator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
