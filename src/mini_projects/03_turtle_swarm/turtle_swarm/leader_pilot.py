import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


CENTER_X = 5.5
CENTER_Y = 5.5
AMP_X = 3.6             # Horizontal size of figure-8
AMP_Y = 2.8             # Vertical size of figure-8
OMEGA = 0.32            # Speed along the figure-8 path (rad/s)

LINEAR_GAIN = 2.0
ANGULAR_GAIN = 5.0
MAX_LINEAR_SPEED = 2.6
MAX_ANGULAR_SPEED = 5.0


class LeaderPilot(Node):
    """Autonomously flies turtle1 along a smooth figure-8 (infinity) trajectory."""

    def __init__(self):
        super().__init__('leader_pilot')
        self.pose = None
        self.t = 0.0
        self.dt = 0.05  # 20 Hz

        self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_timer(self.dt, self.control_loop)

        self.get_logger().info('Leader Pilot started! Tracing figure-8 trajectory on turtle1.')

    def pose_callback(self, msg: Pose):
        self.pose = msg

    def control_loop(self):
        if self.pose is None:
            return

        # Advance parametric time along the Lissajous figure-8 curve
        self.t += self.dt
        x_ref = CENTER_X + AMP_X * math.sin(OMEGA * self.t)
        y_ref = CENTER_Y + AMP_Y * math.sin(2.0 * OMEGA * self.t)

        dx = x_ref - self.pose.x
        dy = y_ref - self.pose.y
        distance = math.hypot(dx, dy)

        desired_angle = math.atan2(dy, dx)
        angle_error = math.atan2(
            math.sin(desired_angle - self.pose.theta),
            math.cos(desired_angle - self.pose.theta),
        )

        cmd = Twist()
        angular_cmd = ANGULAR_GAIN * angle_error
        cmd.angular.z = max(-MAX_ANGULAR_SPEED, min(MAX_ANGULAR_SPEED, angular_cmd))

        alignment = max(0.0, math.cos(angle_error))
        cmd.linear.x = min(MAX_LINEAR_SPEED, LINEAR_GAIN * distance * alignment)

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = LeaderPilot()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
