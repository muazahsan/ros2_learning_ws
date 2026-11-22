from collections import deque
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen, Spawn


# Default turtlesim background color (used as our "eraser ink"!)
BG_RGB = (69, 86, 255)
ERASER_WIDTH = 12       # Wider than writer's pen (4) for a clean wipe

ERASER_HOME_X = 9.5
ERASER_HOME_Y = 5.5
ERASE_DELAY_SEC = 1.2   # Pause briefly so viewer sees the letter before erasing


def wrap_angle(angle: float) -> float:
    return math.atan2(math.sin(angle), math.cos(angle))


class EraserNode(Node):
    """Spawns turtle2 and erases every stroke published on /erase_queue."""

    def __init__(self):
        super().__init__('eraser_node')

        self.pose = None
        self.queue = deque()        # FIFO queue of (x, y, erase_down)
        self.current_target = None  # Active (x, y, erase_down)
        self.pen_is_down = None
        self.wait_until = None

        self.create_subscription(Pose, '/turtle2/pose', self.pose_callback, 10)
        self.create_subscription(Point, '/erase_queue', self.queue_callback, 50)
        self.cmd_pub = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)

        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.pen_client = self.create_client(SetPen, '/turtle2/set_pen')

        self.get_logger().info('Waiting for /spawn service...')
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Still waiting for /spawn...')

        self.spawn_eraser_turtle()

        # 20 Hz closed-loop eraser controller
        self.create_timer(0.05, self.control_loop)
        self.get_logger().info('Eraser ready! Waiting for strokes on /erase_queue...')

    def pose_callback(self, msg: Pose):
        self.pose = msg

    def queue_callback(self, msg: Point):
        # If idle, start a short delay so the letter is visible before erasing
        if self.current_target is None and len(self.queue) == 0:
            now = self.get_clock().now().nanoseconds / 1e9
            self.wait_until = now + ERASE_DELAY_SEC

        erase_down = msg.z > 0.5
        self.queue.append((msg.x, msg.y, erase_down))

    def spawn_eraser_turtle(self):
        req = Spawn.Request()
        req.x = ERASER_HOME_X
        req.y = ERASER_HOME_Y
        req.theta = math.pi
        req.name = 'turtle2'

        future = self.spawn_client.call_async(req)
        future.add_done_callback(self.on_spawn_done)

    def on_spawn_done(self, future):
        try:
            res = future.result()
            self.get_logger().info(f'Spawned eraser robot: {res.name}')
        except Exception as exc:
            self.get_logger().warn(f'turtle2 may already exist: {exc}')
        self.set_eraser_pen(False)

    def set_eraser_pen(self, pen_down: bool):
        if self.pen_is_down == pen_down:
            return
        if not self.pen_client.service_is_ready():
            return
        self.pen_is_down = pen_down
        req = SetPen.Request()
        req.r, req.g, req.b = BG_RGB
        req.width = ERASER_WIDTH
        req.off = 0 if pen_down else 1
        self.pen_client.call_async(req)

    def control_loop(self):
        if self.pose is None:
            return

        # Wait briefly when a new letter starts
        if self.wait_until is not None:
            now = self.get_clock().now().nanoseconds / 1e9
            if now < self.wait_until:
                return
            self.wait_until = None

        # Pop the next waypoint from the FIFO queue if idle
        if self.current_target is None:
            if not self.queue:
                self.set_eraser_pen(False)
                return
            self.current_target = self.queue.popleft()
            _, _, erase_down = self.current_target
            self.set_eraser_pen(erase_down)

        target_x, target_y, _ = self.current_target
        dx = target_x - self.pose.x
        dy = target_y - self.pose.y
        distance = math.hypot(dx, dy)

        if distance < 0.08:
            self.cmd_pub.publish(Twist())
            self.current_target = None
            return

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


def main(args=None):
    rclpy.init(args=args)
    node = EraserNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
