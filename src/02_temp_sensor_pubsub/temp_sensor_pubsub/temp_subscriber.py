import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class TempSubscriber(Node):
    def __init__(self):
        # Give this node a name on the ROS 2 network
        super().__init__('temp_subscriber')

        # Create a subscriber: (MessageType, 'topic_name', callback_function, queue_size)
        self.subscription = self.create_subscription(
            Float32,
            '/temperature',
            self.listener_callback,
            10
        )
        self.get_logger().info('Temperature monitor started!')

    def listener_callback(self, msg):
        temp = msg.data
        if temp > 30.0:
            self.get_logger().warn(f'HIGH TEMP ALERT: {temp} C!')
        else:
            self.get_logger().info(f'Temp OK: {temp} C')


def main(args=None):
    rclpy.init(args=args)
    node = TempSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
