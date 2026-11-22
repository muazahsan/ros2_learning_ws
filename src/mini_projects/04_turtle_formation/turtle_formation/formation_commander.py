import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from turtlesim.msg import Pose


CENTER_X = 5.5
CENTER_Y = 5.5
ORBIT_RADIUS = 2.3     # Leaves room for 2.2-unit wingspan inside [0..11]
OMEGA = 0.35           # Smooth angular speed around the loop (rad/s)

SHAPE_SEQUENCE = ['v', 'diamond', 'line', 'circle']
SHAPE_HOLD_SECONDS = 8.0

LINEAR_GAIN = 2.2
ANGULAR_GAIN = 5.0
MAX_LINEAR_SPEED = 2.5
MAX_ANGULAR_SPEED = 5.0


class FormationCommander(Node):
    """Flies turtle1 in a smooth circular path and cycles swarm formations."""

    def __init__(self):
        super().__init__('formation_commander')
        self.pose = None
        self.t = 0.0
        self.dt = 0.05  # 20 Hz
        self.shape_idx = 0

        self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.shape_pub = self.create_publisher(String, '/swarm/formation', 10)

        self.create_timer(self.dt, self.control_loop)
        self.create_timer(SHAPE_HOLD_SECONDS, self.next_formation)

        self.get_logger().info(
            'Formation Commander started! Flying leader loop & cycling shapes every 8s.'
        )

    def pose_callback(self, msg: Pose):
        self.pose = msg

    def next_formation(self):
        self.shape_idx = (self.shape_idx + 1) % len(SHAPE_SEQUENCE)
        msg = String()
        msg.data = SHAPE_SEQUENCE[self.shape_idx]
        self.shape_pub.publish(msg)
        self.get_logger().info(f"Commanded formation -> '{msg.data.upper()}'")

    def control_loop(self):
        if self.pose is None:
            return

        self.t += self.dt
        x_ref = CENTER_X + ORBIT_RADIUS * math.cos(OMEGA * self.t)
        y_ref = CENTER_Y + ORBIT_RADIUS * math.sin(OMEGA * self.t)

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
    node = FormationCommander()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
