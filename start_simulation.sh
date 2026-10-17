#!/bin/bash
# Starts the Nav2 + Gazebo TurtleBot3 simulation for the delivery robot project
source /opt/ros/jazzy/setup.bash
source ~/delivery_ws/install/setup.bash
pkill -f "gz sim" 2>/dev/null
echo "Starting simulation. Wait for: Managed nodes are active"
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=True params_file:=$HOME/delivery_ws/config/nav2_params.yaml
