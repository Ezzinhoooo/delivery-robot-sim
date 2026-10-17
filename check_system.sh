#!/bin/bash
# Quick health check for the delivery robot simulation
pass=0
fail=0
echo "Warming up ROS 2 discovery..."
ros2 node list > /dev/null 2>&1
sleep 3
check() {
  if eval "$2" > /dev/null 2>&1; then
    echo "[PASS] $1"; pass=$((pass+1))
  else
    echo "[FAIL] $1"; fail=$((fail+1))
  fi
}
check "Node /amcl is running" "ros2 node list | grep -q '^/amcl$'"
check "Node /planner_server is running" "ros2 node list | grep -q '^/planner_server$'"
check "Node /bt_navigator is running" "ros2 node list | grep -q '^/bt_navigator$'"
check "Topic /cmd_vel exists" "ros2 topic list | grep -q '^/cmd_vel$'"
check "Topic /scan exists" "ros2 topic list | grep -q '^/scan$'"
check "Action /navigate_to_pose exists" "ros2 action list | grep -q '^/navigate_to_pose$'"
check "planner_server is active" "ros2 lifecycle get /planner_server | grep -q '^active'"
check "bt_navigator is active" "ros2 lifecycle get /bt_navigator | grep -q '^active'"
check "delivery_robot package is installed" "ros2 pkg prefix delivery_robot"
echo "Passed: $pass   Failed: $fail"
