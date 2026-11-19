# 07_custom_messages

## Goal
Define a custom `.msg` and `.srv` interface package for robot sensor data.
Use your custom message in a Python publisher and subscriber.

## Concepts to learn
- Creating a `rosidl` interface package (`ament_cmake`)
- Writing `.msg` and `.srv` files
- Importing custom messages in Python (`rclpy`)

## Task checklist
- [ ] Create an interface package with a custom `.msg`
- [ ] Build and verify with `ros2 interface show`
- [ ] Use the custom message in a publisher and subscriber
- [ ] Echo the custom topic from CLI

## Break it on purpose
- Forget to add `<depend>` or `rosidl_generate_interfaces` in `CMakeLists.txt` / `package.xml` and inspect the build error.

## What I learned
<!-- Write your own notes here after finishing this project -->
