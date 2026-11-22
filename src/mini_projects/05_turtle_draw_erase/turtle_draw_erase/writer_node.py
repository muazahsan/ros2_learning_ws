import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

from turtle_draw_erase.characters import CHARACTER_STROKES


# Drawing area centered in turtlesim (0..11)
ORIGIN_X = 3.5
ORIGIN_Y = 2.5
CHAR_WIDTH = 4.0
CHAR_HEIGHT = 6.0

# Parking position for turtle1 after drawing so turtle2 can erase cleanly
PARK_X = 1.3
PARK_Y = 5.5

# Writer pen: bright yellow, width 4
WRITER_RGB = (255, 255, 0)
WRITER_WIDTH = 4


def wrap_angle(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


class WriterNode(Node):
    """Draws user-entered characters with turtle1 and streams strokes to /erase_queue."""

    def __init__(self):
        super().__init__('writer_node')
        self.pose = None

        self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.erase_pub = self.create_publisher(Point, '/erase_queue', 50)
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')

        self.get_logger().info('Waiting for /turtle1/set_pen and /turtle1/pose...')
        self.pen_client.wait_for_service()
        while self.pose is None and rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.05)

        self.get_logger().info('Writer ready! turtle1 will draw; turtle2 will erase.')

    def pose_callback(self, msg: Pose):
        self.pose = msg

    def set_pen(self, pen_down: bool):
        req = SetPen.Request()
        req.r, req.g, req.b = WRITER_RGB
        req.width = WRITER_WIDTH
        req.off = 0 if pen_down else 1
        future = self.pen_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

    def publish_erase_point(self, x: float, y: float, erase_down: bool):
        """Send waypoint to eraser_node: z=1.0 means erase, z=0.0 means travel pen-up."""
        pt = Point()
        pt.x = float(x)
        pt.y = float(y)
        pt.z = 1.0 if erase_down else 0.0
        self.erase_pub.publish(pt)

    def drive_to(self, target_x: float, target_y: float):
        """Turn toward (target_x, target_y) and drive straight to it."""
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.02)
            dx = target_x - self.pose.x
            dy = target_y - self.pose.y
            distance = math.hypot(dx, dy)

            if distance < 0.08:
                break

            desired_angle = math.atan2(dy, dx)
            angle_error = wrap_angle(desired_angle - self.pose.theta)

            cmd = Twist()
            if abs(angle_error) > 0.06:
                cmd.angular.z = max(-5.0, min(5.0, 5.5 * angle_error))
                cmd.linear.x = 0.0
            else:
                cmd.angular.z = 2.0 * angle_error
                cmd.linear.x = min(3.2, max(0.6, 3.0 * distance))

            self.cmd_pub.publish(cmd)

        # Full stop at waypoint
        self.cmd_pub.publish(Twist())

    def draw_character(self, ch: str):
        strokes = CHARACTER_STROKES[ch]
        self.get_logger().info(f"Drawing '{ch}' with turtle1...")

        for stroke in strokes:
            # Convert normalized (0..1) points to turtlesim world coordinates
            world_pts = [
                (ORIGIN_X + nx * CHAR_WIDTH, ORIGIN_Y + ny * CHAR_HEIGHT)
                for nx, ny in stroke
            ]

            # Move to start of stroke with pen UP
            start_x, start_y = world_pts[0]
            self.set_pen(False)
            self.drive_to(start_x, start_y)

            # Tell eraser_node where this stroke begins (pen UP travel)
            self.publish_erase_point(start_x, start_y, erase_down=False)

            # Draw the stroke with pen DOWN and stream each segment to eraser_node
            self.set_pen(True)
            for px, py in world_pts[1:]:
                self.drive_to(px, py)
                self.publish_erase_point(px, py, erase_down=True)

        # Lift pen and park turtle1 on the left so turtle2 has a clear stage
        self.set_pen(False)
        self.drive_to(PARK_X, PARK_Y)
        self.get_logger().info(f"Finished drawing '{ch}'! Watch turtle2 erase it.")


def main(args=None):
    rclpy.init(args=args)
    node = WriterNode()
    try:
        while rclpy.ok():
            user_input = input("\nEnter a character (A-Z, 0-9) or 'q' to quit: ").strip().upper()
            if user_input == 'Q':
                break
            if len(user_input) != 1 or user_input not in CHARACTER_STROKES:
                print('Please enter a single letter (A-Z) or digit (0-9).')
                continue
            node.draw_character(user_input)
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
