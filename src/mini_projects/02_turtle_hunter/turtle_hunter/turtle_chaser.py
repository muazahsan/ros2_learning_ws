import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist
from std_msgs.msg import Empty
from turtlesim.msg import Pose
from turtlesim.srv import SetPen


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


class TurtleChaser(Node):
    """Autonomous closed-loop controller that drives turtle1 to catch targets."""

    def __init__(self):
        super().__init__('turtle_chaser')

        # Publishers
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.caught_pub = self.create_publisher(Empty, '/hunter/target_caught', 10)

        # Subscribers
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self._on_pose, 10
        )
        self.target_sub = self.create_subscription(
            Point, '/hunter/target_pose', self._on_target, 10
        )

        # Optional pen color service for colorful pursuit trails
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        self.colors = [
            (0, 255, 255),    # Cyan
            (255, 220, 40),   # Yellow
            (255, 80, 180),   # Pink
            (80, 255, 120),   # Green
            (255, 140, 40),   # Orange
        ]
        self.color_index = 0

        self.pose = None
        self.target = None
        self.caught_sent = False
        self.catch_radius = 0.45

        # 20 Hz closed-loop control timer
        self.create_timer(0.05, self._control_loop)
        self.get_logger().info('Turtle chaser ready! Waiting for targets...')

    def _on_pose(self, msg: Pose):
        self.pose = msg

    def _on_target(self, msg: Point):
        is_new_target = (
            self.target is None
            or abs(msg.x - self.target.x) > 1e-3
            or abs(msg.y - self.target.y) > 1e-3
        )
        if is_new_target:
            self.target = msg
            self.caught_sent = False
            self._cycle_pen_color()
            self.get_logger().info(
                f'Locked onto new target at ({msg.x:.2f}, {msg.y:.2f})'
            )

    def _cycle_pen_color(self):
        if not self.pen_client.service_is_ready():
            return
        r, g, b = self.colors[self.color_index % len(self.colors)]
        self.color_index += 1
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = 3
        req.off = 0
        self.pen_client.call_async(req)

    def _control_loop(self):
        if self.pose is None or self.target is None or self.caught_sent:
            return

        dx = self.target.x - self.pose.x
        dy = self.target.y - self.pose.y
        distance = math.hypot(dx, dy)

        if distance < self.catch_radius:
            self.cmd_pub.publish(Twist())  # Stop turtle1
            self.caught_sent = True
            self.caught_pub.publish(Empty())
            return

        target_angle = math.atan2(dy, dx)
        angle_error = math.atan2(
            math.sin(target_angle - self.pose.theta),
            math.cos(target_angle - self.pose.theta),
        )

        # Smooth curved pursuit: slow down while turning sharply, speed up when aligned
        cmd = Twist()
        cmd.angular.z = clamp(6.0 * angle_error, -5.0, 5.0)
        cmd.linear.x = clamp(2.5 * distance, 0.6, 3.5) * max(0.0, math.cos(angle_error))
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleChaser()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
