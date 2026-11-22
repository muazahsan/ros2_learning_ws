import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from turtlesim.msg import Pose
from turtlesim.srv import SetPen, Spawn


TURTLE_NAMES = ['turtle1', 'turtle2', 'turtle3', 'turtle4', 'turtle5']
FOLLOWERS = TURTLE_NAMES[1:]

# Pen colors (R, G, B, width)
PEN_COLORS = {
    'turtle1': (255, 255, 255, 4),  # White (Leader)
    'turtle2': (0, 255, 255, 3),    # Cyan
    'turtle3': (57, 255, 20, 3),    # Neon Green
    'turtle4': (255, 0, 255, 3),    # Magenta
    'turtle5': (255, 165, 0, 3),    # Orange
}

# Local (x_forward, y_left) offsets in the leader's body frame
FORMATIONS = {
    'v': {
        'turtle2': (-1.0,  1.0),
        'turtle3': (-1.0, -1.0),
        'turtle4': (-2.0,  2.0),
        'turtle5': (-2.0, -2.0),
    },
    'diamond': {
        'turtle2': ( 1.4,  0.0),
        'turtle3': ( 0.0,  1.4),
        'turtle4': ( 0.0, -1.4),
        'turtle5': (-1.4,  0.0),
    },
    'line': {
        'turtle2': ( 0.0,  1.1),
        'turtle3': ( 0.0, -1.1),
        'turtle4': ( 0.0,  2.2),
        'turtle5': ( 0.0, -2.2),
    },
    'circle': {
        'turtle2': ( 1.5,  0.0),
        'turtle3': ( 0.0,  1.5),
        'turtle4': (-1.5,  0.0),
        'turtle5': ( 0.0, -1.5),
    },
}

LINEAR_GAIN = 2.6
ANGULAR_GAIN = 6.0
MAX_LINEAR_SPEED = 4.0
MAX_ANGULAR_SPEED = 6.5
SLOT_TOLERANCE = 0.15
SEPARATION_RADIUS = 0.65


def wrap_angle(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


class FormationController(Node):
    """Transforms follower slots from leader frame to world frame and morphs live."""

    def __init__(self):
        super().__init__('formation_controller')

        self.poses = {}
        self.cmd_pubs = {}
        self.pen_clients = {}
        self.current_formation = 'v'
        self.orbit_angle = 0.0

        # Subscribe to every turtle's pose
        for name in TURTLE_NAMES:
            self.create_subscription(
                Pose,
                f'/{name}/pose',
                lambda msg, n=name: self.pose_callback(n, msg),
                10,
            )
            self.pen_clients[name] = self.create_client(SetPen, f'/{name}/set_pen')

        # Publishers for follower velocity commands
        for name in FOLLOWERS:
            self.cmd_pubs[name] = self.create_publisher(Twist, f'/{name}/cmd_vel', 10)

        # Listen for live formation changes ('v', 'diamond', 'line', 'circle')
        self.create_subscription(
            String, '/swarm/formation', self.formation_callback, 10
        )

        # Wait for /spawn service
        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.get_logger().info('Waiting for /spawn service...')
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Still waiting for /spawn...')

        self.set_pen_color('turtle1')
        self.spawn_followers()

        # 20 Hz closed-loop formation controller
        self.create_timer(0.05, self.control_loop)
        self.get_logger().info(
            "Formation Controller ready! Active shape: 'v' "
            "(publish 'v', 'diamond', 'line', or 'circle' to /swarm/formation)."
        )

    def pose_callback(self, name: str, msg: Pose):
        self.poses[name] = msg

    def formation_callback(self, msg: String):
        shape = msg.data.strip().lower()
        if shape in FORMATIONS:
            if shape != self.current_formation:
                self.current_formation = shape
                self.get_logger().info(f"Morphing swarm into '{shape.upper()}' formation!")
        else:
            self.get_logger().warn(
                f"Unknown formation '{shape}'. Valid options: {list(FORMATIONS.keys())}"
            )

    def spawn_followers(self):
        """Spawn followers around the initial V-formation positions."""
        initial_offsets = FORMATIONS['v']
        for name in FOLLOWERS:
            ox, oy = initial_offsets[name]
            req = Spawn.Request()
            req.x = max(0.8, min(10.2, 5.5 + ox))
            req.y = max(0.8, min(10.2, 5.5 + oy))
            req.theta = 0.0
            req.name = name

            future = self.spawn_client.call_async(req)
            future.add_done_callback(
                lambda fut, n=name: self.on_spawn_done(n, fut)
            )

    def on_spawn_done(self, name: str, future):
        try:
            res = future.result()
            self.get_logger().info(f'Spawned {res.name}')
        except Exception as exc:
            self.get_logger().warn(f'Could not spawn {name} (may already exist): {exc}')
        self.set_pen_color(name)

    def set_pen_color(self, name: str):
        client = self.pen_clients[name]
        if not client.service_is_ready():
            return
        r, g, b, width = PEN_COLORS[name]
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = width
        req.off = 0
        client.call_async(req)

    def control_loop(self):
        if 'turtle1' not in self.poses:
            return

        leader = self.poses['turtle1']
        offsets = FORMATIONS[self.current_formation]

        # Slowly spin the ring when in 'circle' mode
        if self.current_formation == 'circle':
            self.orbit_angle = wrap_angle(self.orbit_angle + 0.04)
            frame_angle = leader.theta + self.orbit_angle
        else:
            frame_angle = leader.theta

        cos_t = math.cos(frame_angle)
        sin_t = math.sin(frame_angle)

        for name in FOLLOWERS:
            if name not in self.poses:
                continue

            follower = self.poses[name]
            local_x, local_y = offsets[name]

            # 2D rotation matrix: Leader body frame -> World frame
            target_x = leader.x + (local_x * cos_t - local_y * sin_t)
            target_y = leader.y + (local_x * sin_t + local_y * cos_t)

            # Simple inter-robot separation repulsion during shape transitions
            for other_name, other_pose in self.poses.items():
                if other_name == name:
                    continue
                rx = follower.x - other_pose.x
                ry = follower.y - other_pose.y
                sep = math.hypot(rx, ry)
                if 0.01 < sep < SEPARATION_RADIUS:
                    push = (SEPARATION_RADIUS - sep) * 0.8
                    target_x += (rx / sep) * push
                    target_y += (ry / sep) * push

            # Keep target safely inside turtlesim bounds
            target_x = max(0.6, min(10.4, target_x))
            target_y = max(0.6, min(10.4, target_y))

            dx = target_x - follower.x
            dy = target_y - follower.y
            distance = math.hypot(dx, dy)

            cmd = Twist()
            if distance > SLOT_TOLERANCE:
                desired_angle = math.atan2(dy, dx)
                angle_error = wrap_angle(desired_angle - follower.theta)

                angular_cmd = ANGULAR_GAIN * angle_error
                cmd.angular.z = max(-MAX_ANGULAR_SPEED, min(MAX_ANGULAR_SPEED, angular_cmd))

                alignment = max(0.0, math.cos(angle_error))
                cmd.linear.x = min(MAX_LINEAR_SPEED, LINEAR_GAIN * distance * alignment)
            else:
                # In slot: align heading with the leader
                heading_error = wrap_angle(leader.theta - follower.theta)
                cmd.linear.x = 0.0
                cmd.angular.z = max(
                    -MAX_ANGULAR_SPEED, min(MAX_ANGULAR_SPEED, 3.0 * heading_error)
                )

            self.cmd_pubs[name].publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = FormationController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
