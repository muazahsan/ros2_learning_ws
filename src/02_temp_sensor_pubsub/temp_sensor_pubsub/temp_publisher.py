import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class TempPublisher(Node):
    def __init__(self):
        # Give this node a name on the ROS 2 network
        super().__init__('temp_publisher')

        # Create a publisher: (MessageType, 'topic_name', queue_size)
        self.publisher_ = self.create_publisher(Float32, '/temperature', 10)

        # Call timer_callback every 1.0 second
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.get_logger().info('Temperature sensor started!')

    def timer_callback(self):
        msg = Float32()
        # Simulate a temperature reading between 20.0 and 40.0 C
        msg.data = round(random.uniform(20.0, 40.0), 1)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data} C')


def main(args=None):
    rclpy.init(args=args)       # Start ROS 2 Python client
    node = TempPublisher()      # Create our node
    rclpy.spin(node)            # Keep node running until Ctrl+C
    node.destroy_node()         # Clean up
    rclpy.shutdown()            # Shut down ROS 2


if __name__ == '__main__':
    main()
