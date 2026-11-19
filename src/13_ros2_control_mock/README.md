# 13_ros2_control_mock

## Goal
Set up `ros2_control` using mock hardware (no physical motors needed).
Send joint position commands through a standard controller.

## Concepts to learn
- `ros2_control` architecture (Hardware Interface, Controller Manager)
- `mock_components/GenericSystem`
- Loading and activating controllers (`joint_state_broadcaster`, `forward_command_controller`)

## Task checklist
- [ ] Add `<ros2_control>` tags to your URDF
- [ ] Write a controller YAML config file
- [ ] Launch `controller_manager` and spawn controllers
- [ ] Send joint commands via `ros2 topic pub`

## Break it on purpose
- Mismatch a joint name between the URDF `<ros2_control>` block and the controller YAML file, then read the controller manager error.

## What I learned
<!-- Write your own notes here after finishing this project -->
