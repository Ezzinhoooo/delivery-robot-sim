import math
import sys

import rclpy
from rclpy.signals import SignalHandlerOptions
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from rclpy.utilities import remove_ros_args

# name: (x, y, yaw) in the map frame, in meters and radians
DELIVERY_POINTS = {
    'base': (-2.0, -0.5, 0.0),
    'A': (0.55, -0.55, 0.0),
    'B': (0.55, 0.55, 0.0),
    'C': (-0.55, 0.55, 0.0),
    'bad': (8.0, 8.0, 0.0),
}


def make_pose(navigator, x, y, yaw):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = math.sin(yaw / 2.0)
    pose.pose.orientation.w = math.cos(yaw / 2.0)
    return pose


def go_to(navigator, name):
    log = navigator.get_logger()
    x, y, yaw = DELIVERY_POINTS[name]
    log.info(f'Heading to {name} at ({x}, {y})')

    accepted = navigator.goToPose(make_pose(navigator, x, y, yaw))
    if not accepted:
        log.error(f'Nav2 REJECTED the goal for {name}.')
        return False

    ticks = 0
    while not navigator.isTaskComplete():
        ticks += 1
        feedback = navigator.getFeedback()
        if feedback and ticks % 10 == 0:
            log.info(f'  {name}: {feedback.distance_remaining:.2f} m remaining')

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        log.info(f'Arrived at {name}.')
        return True
    if result == TaskResult.CANCELED:
        log.warn(f'Trip to {name} was canceled.')
    else:
        log.error(f'Trip to {name} FAILED (Nav2 aborted the goal).')
    return False


def main(args=None):
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    stops = remove_ros_args(sys.argv)[1:]

    if not stops:
        print('Usage: ros2 run delivery_robot delivery_mission STOP [STOP ...]')
        print('Available stops: ' + ', '.join(DELIVERY_POINTS.keys()))
        rclpy.shutdown()
        return
    unknown = [s for s in stops if s not in DELIVERY_POINTS]
    if unknown:
        print('Unknown stop(s): ' + ', '.join(unknown))
        print('Available stops: ' + ', '.join(DELIVERY_POINTS.keys()))
        rclpy.shutdown()
        return

    navigator = BasicNavigator()
    log = navigator.get_logger()
    log.info('Waiting for Nav2 to become active...')
    navigator.waitUntilNav2Active(localizer='bt_navigator')

    delivered = []
    failed_at = None
    try:
        for stop in stops:
            if go_to(navigator, stop):
                delivered.append(stop)
            else:
                failed_at = stop
                break

        log.info('Returning to base...')
        back_home = go_to(navigator, 'base')
    except KeyboardInterrupt:
        log.warn('Interrupted by user, canceling the current goal.')
        navigator.cancelTask()
        back_home = False

    log.info('---- Mission summary ----')
    log.info('Delivered: ' + (', '.join(delivered) if delivered else 'none'))
    if failed_at:
        log.error(f'Mission stopped at: {failed_at}')
    log.info('Back at base: ' + ('yes' if back_home else 'NO'))

    navigator.destroy_node()
    if rclpy.ok():
        rclpy.shutdown()
