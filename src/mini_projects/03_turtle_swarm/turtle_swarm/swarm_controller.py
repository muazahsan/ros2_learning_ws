import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen, Spawn


# Leader + 4 followers = 5-robot convoy
TURTLE_NAMES = ['turtle1', 'turtle2', 'turtle3', 'turtle4', 'turtle5']

# Bright pen colors (R, G, B, width) so each robot's trail stands out
PEN_COLORS = {
    'turtle1': (255, 255, 255, 4),  # White (Leader)
    'turtle2': (0, 255, 255, 3),    # Cyan
    'turtle3': (57, 255, 20, 3),    # Neon Green
    'turtle4': (255, 0, 255, 3),    # Magenta
    'turtle5': (255, 165, 0, 3),    # Orange
}

SAFE_DISTANCE = 1.0       # Minimum gap between consecutive turtles
LINEAR_GAIN = 2.2         # Proportional gain for forward speed
ANGULAR_GAIN = 5.0        # Proportional gain for turning speed
MAX_LINEAR_SPEED = 3.5    # Clamp max linear velocity
MAX_ANGULAR_SPEED = 6.0   # Clamp max angular velocity


class SwarmController(Node):
    """Spawns follower turtles and drives them in a leader-follower convoy."""

    def __init__(self):
        super().__init__('swarm_controller')

        # Latest Pose for each turtle in the swarm
        self.poses = {}

        # Publishers (cmd_vel) and pen service clients for followers
        self.cmd_pubs = {}
        self.pen_clients = {}

        # Subscribe to every turtle's pose topic (including leader turtle1)
        for name in TURTLE_NAMES:
            self.create_subscription(
                Pose,
                f'/{name}/pose',
                lambda msg, n=name: self.pose_callback(n, msg),
                10,
            )
            self.pen_clients[name] = self.create_client(SetPen, f'/{name}/set_pen')

        # Create cmd_vel publishers only for followers (turtle2..turtle5)
        for follower in TURTLE_NAMES[1:]:
            self.cmd_pubs[follower] = self.create_publisher(
                Twist, f'/{follower}/cmd_vel', 10
            )

        # Wait for turtlesim /spawn service
        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.get_logger().info('Waiting for /spawn service...')
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Still waiting for /spawn...')

        # Set leader pen color, then spawn all followers behind turtle1
        self.set_pen_color('turtle1')
        self.spawn_followers()

        # 20 Hz closed-loop convoy controller
        self.create_timer(0.05, self.control_loop)
        self.get_logger().info(
            'Swarm Controller active! Drive turtle1 with leader_pilot or turtle_teleop_key.'
        )

    def pose_callback(self, name: str, msg: Pose):
        self.poses[name] = msg

    def spawn_followers(self):
        """Spawn turtle2..turtle5 neatly lined up behind turtle1."""
        for idx, name in enumerate(TURTLE_NAMES[1:], start=1):
            req = Spawn.Request()
            req.x = max(0.8, 5.5 - (idx * SAFE_DISTANCE))
            req.y = 5.5
            req.theta = 0.0
            req.name = name

            future = self.spawn_client.call_async(req)
            future.add_done_callback(
                lambda fut, n=name: self.on_spawn_done(n, fut)
            )

    def on_spawn_done(self, name: str, future):
        try:
            res = future.result()
            self.get_logger().info(f'Spawned follower: {res.name}')
            self.set_pen_color(name)
        except Exception as exc:
            self.get_logger().warn(f'Could not spawn {name} (maybe already exists): {exc}')
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
        """Each follower chases the turtle directly in front of it."""
        for i in range(1, len(TURTLE_NAMES)):
            leader_name = TURTLE_NAMES[i - 1]
            follower_name = TURTLE_NAMES[i]

            if leader_name not in self.poses or follower_name not in self.poses:
                continue

            leader = self.poses[leader_name]
            follower = self.poses[follower_name]

            dx = leader.x - follower.x
            dy = leader.y - follower.y
            distance = math.hypot(dx, dy)

            cmd = Twist()

            if distance > SAFE_DISTANCE:
                desired_angle = math.atan2(dy, dx)
                angle_error = math.atan2(
                    math.sin(desired_angle - follower.theta),
                    math.cos(desired_angle - follower.theta),
                )

                # Turn smoothly toward the robot ahead
                angular_cmd = ANGULAR_GAIN * angle_error
                cmd.angular.z = max(-MAX_ANGULAR_SPEED, min(MAX_ANGULAR_SPEED, angular_cmd))

                # Drive forward proportionally to extra gap, scaled by alignment
                gap = distance - SAFE_DISTANCE
                alignment = max(0.0, math.cos(angle_error))
                cmd.linear.x = min(MAX_LINEAR_SPEED, LINEAR_GAIN * gap * alignment)
            else:
                # Inside safe gap: hold position to prevent collisions
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0

            self.cmd_pubs[follower_name].publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = SwarmController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
