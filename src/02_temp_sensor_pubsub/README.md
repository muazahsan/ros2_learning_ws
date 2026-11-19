# 02_temp_sensor_pubsub

## Goal
Build a Python publisher that simulates a temperature sensor.
Build a subscriber that reads the temperature and prints a warning if it gets too high.

## Concepts to learn
- ROS 2 Python package structure (`ament_python`)
- `rclpy` Node, Publisher, Subscriber, and Timer
- Standard messages (`std_msgs/msg/Float32`)

## Task checklist
- [ ] Create a ROS 2 Python package
- [ ] Write the temperature publisher node
- [ ] Write the temperature monitor subscriber node
- [ ] Build with `colcon build` and run both nodes
- [ ] Verify data flow with `ros2 topic echo` and `rqt_graph`

## Break it on purpose
- Change the topic name in the subscriber so it does not match the publisher, then diagnose it using `ros2 topic list` and `rqt_graph`.

## What I learned
<!-- Write your own notes here after finishing this project -->
