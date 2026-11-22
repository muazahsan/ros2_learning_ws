import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from turtlesim.msg import Pose
from turtlesim.srv import SetPen


def wrap_angle(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


def make_arc(cx: float, cy: float, radius: float,
             start_deg: float, end_deg: float, steps: int):
    """Generate (x, y) waypoints along a circular arc from start_deg to end_deg."""
    points = []
    for i in range(steps + 1):
        deg = start_deg + (end_deg - start_deg) * (i / steps)
        rad = math.radians(deg)
        points.append((cx + radius * math.cos(rad), cy + radius * math.sin(rad)))
    return points


class SmileyDrawer(Node):
    """Draws a colorful smiley face in turtlesim using parametric circle & arc paths."""

    def __init__(self):
        super().__init__('smiley_drawer')
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

    def set_pen(self, r: int, g: int, b: int, width: int, pen_down: bool):
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = width
        req.off = 0 if pen_down else 1
        future = self.pen_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

    def drive_to(self, target_x: float, target_y: float,
                 stop_at_end: bool = True, tolerance: float = 0.12):
        """Closed-loop controller to drive turtle1 to (target_x, target_y)."""
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.02)
            dx = target_x - self.pose.x
            dy = target_y - self.pose.y
            distance = math.hypot(dx, dy)

            if distance < tolerance:
                break

            desired_angle = math.atan2(dy, dx)
            angle_error = wrap_angle(desired_angle - self.pose.theta)

            cmd = Twist()
            cmd.angular.z = max(-6.0, min(6.0, 6.0 * angle_error))
            alignment = max(0.0, math.cos(angle_error))
            cmd.linear.x = min(3.2, max(0.5, 3.0 * distance) * alignment)
            self.cmd_pub.publish(cmd)

        if stop_at_end:
            self.cmd_pub.publish(Twist())

    def draw_stroke(self, points, rgb, width: int, label: str):
        self.get_logger().info(f'Drawing {label}...')
        r, g, b = rgb

        # Move to start of stroke with pen UP
        self.set_pen(r, g, b, width, pen_down=False)
        self.drive_to(points[0][0], points[0][1], stop_at_end=True, tolerance=0.08)

        # Lower pen and trace smoothly through every point
        self.set_pen(r, g, b, width, pen_down=True)
        for idx, (px, py) in enumerate(points[1:], start=1):
            is_last = (idx == len(points) - 1)
            self.drive_to(px, py, stop_at_end=is_last, tolerance=0.14 if not is_last else 0.08)

    def draw_smiley(self):
        self.clear_canvas()

        # 1. Face outline: bright yellow circle centered at (5.5, 5.5)
        face = make_arc(5.5, 5.5, radius=3.5, start_deg=0, end_deg=360, steps=40)
        self.draw_stroke(face, rgb=(255, 220, 0), width=6, label='face outline')

        # 2. Left eye: bold dark circle
        left_eye = make_arc(4.2, 6.7, radius=0.45, start_deg=0, end_deg=360, steps=18)
        self.draw_stroke(left_eye, rgb=(20, 20, 20), width=8, label='left eye')

        # 3. Right eye: bold dark circle
        right_eye = make_arc(6.8, 6.7, radius=0.45, start_deg=0, end_deg=360, steps=18)
        self.draw_stroke(right_eye, rgb=(20, 20, 20), width=8, label='right eye')

        # 4. Big happy smile: smooth bottom arc (210° to 330°)
        smile = make_arc(5.5, 5.6, radius=2.1, start_deg=210, end_deg=330, steps=24)
        self.draw_stroke(smile, rgb=(255, 70, 70), width=7, label='big smile')

        # 5. Park neatly in the bottom-left corner so the face is unobstructed
        self.set_pen(255, 220, 0, 4, pen_down=False)
        self.drive_to(1.0, 1.0, stop_at_end=True, tolerance=0.1)
        self.get_logger().info('Smiley face complete! :)')


def main(args=None):
    rclpy.init(args=args)
    node = SmileyDrawer()
    try:
        node.draw_smiley()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
