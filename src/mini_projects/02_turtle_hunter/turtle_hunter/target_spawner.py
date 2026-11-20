import math
import random

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from std_msgs.msg import Empty
from turtlesim.srv import Kill, Spawn


class TargetSpawner(Node):
    """Spawns random target turtles, tracks score, and respawns on catch."""

    def __init__(self):
        super().__init__('target_spawner')

        # Service clients for turtlesim
        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.kill_client = self.create_client(Kill, '/kill')

        # Publisher: broadcasts the active target's (x, y) position
        self.target_pub = self.create_publisher(Point, '/hunter/target_pose', 10)

        # Subscriber: listens for catch notifications from turtle_chaser
        self.caught_sub = self.create_subscription(
            Empty, '/hunter/target_caught', self._on_target_caught, 10
        )

        self.score = 0
        self.target_id = 0
        self.current_target_name = None
        self.current_target_point = None
        self.busy = False

        self.get_logger().info('Waiting for turtlesim /spawn and /kill services...')
        self.spawn_client.wait_for_service()
        self.kill_client.wait_for_service()
        self.get_logger().info('Connected to turtlesim! Starting hunt...')

        # Spawn the first target and broadcast its position at 5 Hz
        self._spawn_new_target()
        self.create_timer(0.2, self._publish_target_pose)

    def _publish_target_pose(self):
        if self.current_target_point is not None and not self.busy:
            self.target_pub.publish(self.current_target_point)

    def _spawn_new_target(self):
        self.busy = True
        self.target_id += 1
        name = f'target_{self.target_id}'

        req = Spawn.Request()
        req.x = random.uniform(1.5, 9.5)
        req.y = random.uniform(1.5, 9.5)
        req.theta = random.uniform(0.0, 2.0 * math.pi)
        req.name = name

        future = self.spawn_client.call_async(req)
        future.add_done_callback(
            lambda f: self._on_spawn_done(f, name, req.x, req.y)
        )

    def _on_spawn_done(self, future, name: str, x: float, y: float):
        try:
            future.result()
        except Exception as exc:
            self.get_logger().error(f'Failed to spawn {name}: {exc}')
            self.busy = False
            return

        self.current_target_name = name
        self.current_target_point = Point(x=x, y=y, z=0.0)
        self.busy = False
        self.get_logger().info(f'Spawned {name} at ({x:.2f}, {y:.2f})')

    def _on_target_caught(self, _msg: Empty):
        if self.busy or self.current_target_name is None:
            return

        self.busy = True
        self.score += 1
        caught_name = self.current_target_name
        self.current_target_point = None
        self.get_logger().info(f'CAUGHT {caught_name}! | Score: {self.score}')

        req = Kill.Request()
        req.name = caught_name
        future = self.kill_client.call_async(req)
        future.add_done_callback(self._on_kill_done)

    def _on_kill_done(self, future):
        try:
            future.result()
        except Exception as exc:
            self.get_logger().warn(f'Kill service warning: {exc}')

        self.current_target_name = None
        self._spawn_new_target()


def main(args=None):
    rclpy.init(args=args)
    node = TargetSpawner()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
