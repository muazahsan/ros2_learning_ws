# 05_parameters

## Goal
Make a node configurable at runtime using ROS 2 parameters.
Change publish rate and threshold values without editing or rebuilding code.

## Concepts to learn
- Declaring and reading parameters in `rclpy`
- Setting parameters via CLI and YAML files
- Dynamic parameter callbacks

## Task checklist
- [ ] Add parameters to a node (e.g., `publish_rate`, `max_temp`)
- [ ] Inspect and change parameters with `ros2 param`
- [ ] Save and load parameters from a YAML file
- [ ] Add a callback to react to live parameter changes

## Break it on purpose
- Pass a string value to a parameter declared as a float/int and read the type error.

## What I learned
<!-- Write your own notes here after finishing this project -->
