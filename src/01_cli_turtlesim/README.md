# 01_cli_turtlesim

## Goal
Control a simulated turtle using ROS 2 CLI tools.
Learn how nodes, topics, services, and rqt_graph work without writing code.

## Concepts to learn
- ROS 2 nodes and topics
- CLI commands (`ros2 node`, `ros2 topic`, `ros2 service`)
- Visualizing graphs with `rqt_graph`

## Task checklist
- [ ] Run `turtlesim_node` and `turtle_teleop_key`
- [ ] Inspect active nodes and topics
- [ ] Publish velocity commands from the terminal
- [ ] Call a service to spawn a second turtle
- [ ] View the system in `rqt_graph`

## Break it on purpose
- Publish a `geometry_msgs/msg/Twist` message with the wrong field name or wrong topic name and observe what happens.

## What I learned
<!-- Write your own notes here after finishing this project -->
