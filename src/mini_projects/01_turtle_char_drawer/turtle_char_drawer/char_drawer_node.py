import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

from turtle_char_drawer.characters import CHARACTER_STROKES


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


class TurtleCharDrawer(Node):
    """ROS 2 node that drives turtle1 in turtlesim to draw a character."""

    def __init__(self):
        super().__init__('turtle_char_drawer')

        # 1. Publisher: send velocity commands to move turtle1
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # 2. Subscriber: read turtle1's live (x, y, theta) position
        self.pose = None
        self.pose_sub = self.create_subscription(
            Pose, '/turtle1/pose', self._pose_callback, 10
        )

        # 3. Service clients: lift/lower pen and clear the screen
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        self.clear_client = self.create_client(Empty, '/clear')

        # Drawing box inside the 11.08 x 11.08 turtlesim window
        self.origin_x = 3.5
        self.origin_y = 3.0
        self.width = 4.0
        self.height = 5.0

    def _pose_callback(self, msg: Pose):
        self.pose = msg

    def wait_for_turtlesim(self):
        """Wait until turtlesim services and pose topic are ready."""
        self.get_logger().info('Waiting for turtlesim node...')
        self.pen_client.wait_for_service()
        self.clear_client.wait_for_service()
        while rclpy.ok() and self.pose is None:
            rclpy.spin_once(self, timeout_sec=0.05)
        self.get_logger().info('Connected to turtlesim!')

    def clear_screen(self):
        """Call /clear service to wipe old drawings."""
        future = self.clear_client.call_async(Empty.Request())
        rclpy.spin_until_future_complete(self, future)

    def set_pen(self, pen_on: bool, r: int = 255, g: int = 220, b: int = 40, width: int = 4):
        """Call /turtle1/set_pen service to lift (off=1) or lower (off=0) the pen."""
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = width
        req.off = 0 if pen_on else 1
        future = self.pen_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

    def stop_turtle(self):
        """Publish zero velocity to stop turtle1."""
        self.cmd_pub.publish(Twist())

    def move_to(self, target_x: float, target_y: float):
        """Turn toward (target_x, target_y) and drive straight to it."""
        dist_tolerance = 0.05
        angle_tolerance = 0.03

        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.02)

            dx = target_x - self.pose.x
            dy = target_y - self.pose.y
            distance = math.hypot(dx, dy)

            if distance < dist_tolerance:
                break

            target_angle = math.atan2(dy, dx)
            angle_error = math.atan2(
                math.sin(target_angle - self.pose.theta),
                math.cos(target_angle - self.pose.theta),
            )

            cmd = Twist()
            if abs(angle_error) > angle_tolerance:
                # Step 1: Rotate in place until facing the target
                cmd.angular.z = clamp(6.0 * angle_error, -4.0, 4.0)
            else:
                # Step 2: Drive straight toward the target
                cmd.linear.x = clamp(4.0 * distance, 0.4, 4.0)
                cmd.angular.z = clamp(4.0 * angle_error, -2.0, 2.0)

            self.cmd_pub.publish(cmd)

        self.stop_turtle()

    def draw_character(self, char: str):
        """Clear the canvas and draw all strokes for the given character."""
        strokes = CHARACTER_STROKES[char]
        self.get_logger().info(f'Drawing character: {char}')

        self.set_pen(pen_on=False)
        self.clear_screen()

        for stroke in strokes:
            # Convert normalized (0..1) points to turtlesim coordinates
            world_points = [
                (self.origin_x + nx * self.width, self.origin_y + ny * self.height)
                for (nx, ny) in stroke
            ]

            # Move to the start of the stroke with pen UP
            self.set_pen(pen_on=False)
            self.move_to(*world_points[0])

            # Put pen DOWN and draw through the rest of the stroke
            self.set_pen(pen_on=True)
            for point in world_points[1:]:
                self.move_to(*point)

        # Lift pen when finished
        self.set_pen(pen_on=False)
        self.get_logger().info(f'Finished drawing: {char}')


def main(args=None):
    rclpy.init(args=args)
    node = TurtleCharDrawer()

    try:
        node.wait_for_turtlesim()
        print('\n=== Turtlesim Character Drawer ===')
        print('Type a single letter (A-Z) or number (0-9), then press Enter.')
        print('Type "quit" to exit.\n')

        while rclpy.ok():
            user_input = input('Enter character: ').strip().upper()
            if user_input in ('QUIT', 'EXIT'):
                break
            if len(user_input) != 1 or user_input not in CHARACTER_STROKES:
                print('Please enter ONE character from A-Z or 0-9.')
                continue

            node.draw_character(user_input)
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        node.stop_turtle()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
