import math

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

GOAL_X = 0.55
GOAL_Y = -0.55
GOAL_YAW = 0.0


def make_pose(navigator, x, y, yaw):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = math.sin(yaw / 2.0)
    pose.pose.orientation.w = math.cos(yaw / 2.0)
    return pose


def main(args=None):
    rclpy.init(args=args)
    navigator = BasicNavigator()
    log = navigator.get_logger()

    log.info('Waiting for Nav2 to become active...')
    navigator.waitUntilNav2Active(localizer='bt_navigator')

    goal = make_pose(navigator, GOAL_X, GOAL_Y, GOAL_YAW)
    log.info(f'Sending goal: x={GOAL_X}, y={GOAL_Y}')
    navigator.goToPose(goal)

    ticks = 0
    while not navigator.isTaskComplete():
        ticks += 1
        feedback = navigator.getFeedback()
        if feedback and ticks % 10 == 0:
            log.info(f'Distance remaining: {feedback.distance_remaining:.2f} m')

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        log.info('Delivery goal reached!')
    elif result == TaskResult.CANCELED:
        log.warn('Goal was canceled.')
    elif result == TaskResult.FAILED:
        log.error('Goal failed (rejected or aborted by Nav2).')
    else:
        log.error('Goal ended with an unknown status.')

    navigator.destroy_node()
    rclpy.shutdown()
