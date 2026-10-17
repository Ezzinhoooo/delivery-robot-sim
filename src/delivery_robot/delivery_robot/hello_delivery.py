import rclpy
from rclpy.node import Node


class HelloDelivery(Node):
    def __init__(self):
        super().__init__('hello_delivery')
        self.get_logger().info('Hello! The delivery_robot node is alive.')
        self.counter = 0
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        self.counter += 1
        self.get_logger().info(f'Still running... tick {self.counter}')


def main(args=None):
    rclpy.init(args=args)
    node = HelloDelivery()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
