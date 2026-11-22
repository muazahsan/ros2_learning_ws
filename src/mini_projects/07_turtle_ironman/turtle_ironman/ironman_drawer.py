import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from turtlesim.msg import Pose
from turtlesim.srv import SetPen


# Iron Man color palette (R, G, B)
RED = (220, 25, 25)
GOLD = (255, 200, 30)
CYAN = (0, 245, 255)
WHITE = (255, 255, 255)
DARK = (30, 30, 40)

# Layered symmetric Iron Man helmet geometry centered at x = 5.5
IRONMAN_LAYERS = [
    (
        'outer red helmet',
        RED,
        6,
        [
            (5.5, 9.8), (6.8, 9.6), (7.9, 8.8), (8.5, 7.5),
            (8.6, 5.8), (8.2, 4.2), (7.6, 2.7), (6.7, 1.5),
            (6.1, 1.1), (4.9, 1.1), (4.3, 1.5), (3.4, 2.7),
            (2.8, 4.2), (2.4, 5.8), (2.5, 7.5), (3.1, 8.8),
            (4.2, 9.6), (5.5, 9.8),
        ],
    ),
    (
        'gold faceplate',
        GOLD,
        5,
        [
            (4.8, 7.9), (6.2, 7.9), (6.2, 9.1), (7.3, 8.5),
            (7.8, 7.2), (7.6, 6.2), (8.0, 5.1), (7.3, 3.6),
            (6.8, 2.3), (6.1, 1.6), (4.9, 1.6), (4.2, 2.3),
            (3.7, 3.6), (3.0, 5.1), (3.4, 6.2), (3.2, 7.2),
            (3.7, 8.5), (4.8, 9.1), (4.8, 7.9),
        ],
    ),
    (
        'left cheek armor line',
        DARK,
        3,
        [(3.4, 5.0), (4.4, 4.2), (4.4, 2.9)],
    ),
    (
        'right cheek armor line',
        DARK,
        3,
        [(7.6, 5.0), (6.6, 4.2), (6.6, 2.9)],
    ),
    (
        'mouth slit',
        DARK,
        4,
        [(4.4, 2.9), (4.9, 3.1), (6.1, 3.1), (6.6, 2.9)],
    ),
    (
        'chin plate',
        DARK,
        3,
        [(4.6, 2.2), (5.0, 2.4), (6.0, 2.4), (6.4, 2.2)],
    ),
    (
        'left brow ridge',
        DARK,
        3,
        [(3.3, 6.6), (4.8, 6.2), (5.2, 7.9)],
    ),
    (
        'right brow ridge',
        DARK,
        3,
        [(7.7, 6.6), (6.2, 6.2), (5.8, 7.9)],
    ),
    (
        'left glowing eye',
        CYAN,
        6,
        [(3.5, 6.2), (5.0, 5.8), (4.8, 5.4), (3.7, 5.6), (3.5, 6.2)],
    ),
    (
        'left eye core glow',
        WHITE,
        2,
        [(3.75, 5.9), (4.85, 5.65)],
    ),
    (
        'right glowing eye',
        CYAN,
        6,
        [(7.5, 6.2), (6.0, 5.8), (6.2, 5.4), (7.3, 5.6), (7.5, 6.2)],
    ),
    (
        'right eye core glow',
        WHITE,
        2,
        [(7.25, 5.9), (6.15, 5.65)],
    ),
]


def wrap_angle(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


class IronManDrawer(Node):
    """Draws Iron Man's red-and-gold helmet with glowing cyan eyes in turtlesim."""

    def __init__(self):
        super().__init__('ironman_drawer')
        self.pose = None

        self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        self.clear_client = self.create_client(Empty, '/clear')

        self.get_logger().info('Waiting for turtlesim services and /turtle1/pose...')
        self.pen_client.wait_for_service()
        self.clear_client.wait_for_service()
        while self.pose is None and rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.05)

    def pose_callback(self, msg: Pose):
        self.pose = msg

    def clear_canvas(self):
        future = self.clear_client.call_async(Empty.Request())
        rclpy.spin_until_future_complete(self, future)

    def set_pen(self, rgb, width: int, pen_down: bool):
        r, g, b = rgb
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = width
        req.off = 0 if pen_down else 1
        future = self.pen_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

    def drive_to(self, target_x: float, target_y: float):
        """Sharp turn-then-drive controller for crisp geometric armor corners."""
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.02)
            dx = target_x - self.pose.x
            dy = target_y - self.pose.y
            distance = math.hypot(dx, dy)

            if distance < 0.06:
                break

            desired_angle = math.atan2(dy, dx)
            angle_error = wrap_angle(desired_angle - self.pose.theta)

            cmd = Twist()
            if abs(angle_error) > 0.05:
                cmd.angular.z = max(-5.5, min(5.5, 6.0 * angle_error))
                cmd.linear.x = 0.0
            else:
                cmd.angular.z = 2.0 * angle_error
                cmd.linear.x = min(3.4, max(0.5, 3.2 * distance))

            self.cmd_pub.publish(cmd)

        self.cmd_pub.publish(Twist())

    def draw_ironman(self):
        self.clear_canvas()
        self.get_logger().info('Initializing Mark 85 helmet plotter...')

        for label, rgb, width, points in IRONMAN_LAYERS:
            self.get_logger().info(f'Drawing {label}...')
            self.set_pen(rgb, width, pen_down=False)
            self.drive_to(points[0][0], points[0][1])

            self.set_pen(rgb, width, pen_down=True)
            for px, py in points[1:]:
                self.drive_to(px, py)

        # Park turtle1 neatly in the corner
        self.set_pen(GOLD, 4, pen_down=False)
        self.drive_to(1.0, 1.0)
        self.get_logger().info('Iron Man helmet complete!')


def main(args=None):
    rclpy.init(args=args)
    node = IronManDrawer()
    try:
        node.draw_ironman()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
