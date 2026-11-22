import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from std_msgs.msg import Bool
from turtlesim.srv import Kill, SetPen, Spawn, TeleportAbsolute


# 5 static obstacles arranged in a classic slalom field
OBSTACLES = [
    ('obs_center', 5.5, 5.5),
    ('obs_ul', 3.6, 7.3),
    ('obs_ur', 7.4, 7.3),
    ('obs_ll', 3.6, 3.7),
    ('obs_lr', 7.4, 3.7),
]

# Corner goals across the obstacle field
GOALS = [
    (9.5, 9.5),
    (1.5, 1.5),
    (9.5, 1.5),
    (1.5, 9.5),
]


class ObstacleManager(Node):
    """Spawns static obstacles + goal marker and cycles goals when reached."""

    def __init__(self):
        super().__init__('obstacle_manager')
        self.goal_idx = 0
        self.goals_reached = 0

        self.goal_pub = self.create_publisher(Point, '/apf/goal', 10)
        self.create_subscription(Bool, '/apf/goal_reached', self.on_goal_reached, 10)

        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.kill_client = self.create_client(Kill, '/kill')
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        self.tp_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')

        self.get_logger().info('Waiting for turtlesim services...')
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Still waiting for /spawn...')

        self.setup_arena()

        # Continuously broadcast active goal at 5 Hz so late subscribers receive it
        self.create_timer(0.2, self.publish_goal)

    def setup_arena(self):
        # Move turtle1 cleanly to bottom-left start corner with pen OFF
        if self.pen_client.wait_for_service(timeout_sec=2.0):
            pen_off = SetPen.Request()
            pen_off.r, pen_off.g, pen_off.b, pen_off.width, pen_off.off = 0, 255, 255, 3, 1
            self.pen_client.call_async(pen_off)

        if self.tp_client.wait_for_service(timeout_sec=2.0):
            tp = TeleportAbsolute.Request()
            tp.x, tp.y, tp.theta = 1.5, 1.5, math.pi / 4.0
            fut = self.tp_client.call_async(tp)
            fut.add_done_callback(self._enable_turtle1_pen)

        # Spawn all 5 static obstacle turtles
        for name, ox, oy in OBSTACLES:
            req = Spawn.Request()
            req.name = name
            req.x = ox
            req.y = oy
            req.theta = 0.0
            self.spawn_client.call_async(req)

        # Spawn visual marker turtle at first goal
        self.spawn_goal_marker()
        self.get_logger().info('Arena ready: 5 obstacles + goal marker spawned!')

    def _enable_turtle1_pen(self, _future):
        pen_on = SetPen.Request()
        pen_on.r, pen_on.g, pen_on.b, pen_on.width, pen_on.off = 0, 255, 255, 3, 0
        self.pen_client.call_async(pen_on)

    def spawn_goal_marker(self):
        gx, gy = GOALS[self.goal_idx]
        req = Spawn.Request()
        req.name = 'goal_marker'
        req.x = gx
        req.y = gy
        req.theta = 0.0
        self.spawn_client.call_async(req)

    def publish_goal(self):
        gx, gy = GOALS[self.goal_idx]
        pt = Point()
        pt.x = gx
        pt.y = gy
        pt.z = 0.0
        self.goal_pub.publish(pt)

    def on_goal_reached(self, msg: Bool):
        if not msg.data:
            return
        self.goals_reached += 1
        self.goal_idx = (self.goal_idx + 1) % len(GOALS)
        gx, gy = GOALS[self.goal_idx]
        self.get_logger().info(
            f'Goal #{self.goals_reached} reached! Next goal -> ({gx:.1f}, {gy:.1f})'
        )

        # Respawn goal marker at new goal position
        kill_req = Kill.Request()
        kill_req.name = 'goal_marker'
        fut = self.kill_client.call_async(kill_req)
        fut.add_done_callback(lambda _f: self.spawn_goal_marker())


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
