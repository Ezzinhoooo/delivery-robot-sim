# Autonomous Delivery Robot (ROS 2 Jazzy simulation)

A simulated wheeled robot that drives itself between named delivery points
and returns to base. Runs entirely in simulation (no hardware needed).

Stack: Ubuntu 24.04 (WSL2), ROS 2 Jazzy, Gazebo Harmonic, Nav2, RViz, Python.

## Start the simulation (terminal 1)

    ~/delivery_ws/start_simulation.sh

Wait for "Managed nodes are active".

## Run a delivery mission (terminal 2)

    ros2 run delivery_robot delivery_mission A B C

Stops: base, A, B, C (and "bad", an unreachable point used to test failures).
The robot visits each stop in order, then returns to base.
Press Ctrl+C to cancel the current goal safely.

## Health check

    ~/delivery_ws/check_system.sh

## What I wrote vs. what ROS 2 provides

Written by me:
- delivery_robot package (Python): delivery_mission.py, go_to_goal.py, hello_delivery.py
- config/nav2_params.yaml: copy of Nav2 defaults plus an automatic AMCL start pose
- start_simulation.sh and check_system.sh

Provided by ROS 2 and the community:
- Nav2 (planning, control, localization, behavior tree), Gazebo, RViz
- TurtleBot3 robot model and world, nav2_simple_commander

## How the parts fit together

    delivery_mission.py (my node)
        -> action /navigate_to_pose -> bt_navigator
        -> planner_server computes a path on the map
        -> controller_server publishes velocity on /cmd_vel
        -> Gazebo moves the simulated robot
    Gazebo lidar (/scan) + odometry -> AMCL localizes the robot on the map
    RViz only displays the result.

## ROS 2 concepts demonstrated

Nodes, topics, actions (goal, feedback, result, cancel), lifecycle nodes,
parameters, launch files, TF frames, simulation time, workspaces, packages.

## Test checklist

- [ ] check_system.sh reports 9 passed, 0 failed
- [ ] A, then B C, completes and returns to base
- [ ] "bad" fails clearly, mission stops, robot returns to base
- [ ] Unknown stop name prints usage and does not move the robot
- [ ] Ctrl+C stops the robot and exits cleanly
