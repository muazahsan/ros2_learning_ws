# 15_final_scara_twin

## Goal
Build a digital twin of a SCARA robot combining URDF, Gazebo, `ros2_control`, and a Python control node.
Include a software emergency stop (E-stop) service before any motion.

## Concepts to learn
- Full ROS 2 system integration
- SCARA kinematics and joint control
- Safety E-stop service and state monitoring

## Task checklist
- [ ] Model a 3-DOF/4-DOF SCARA robot in Xacro
- [ ] Simulate in Gazebo with `ros2_control`
- [ ] Write a Python motion + E-stop node
- [ ] Test full workflow and verify with `rqt_graph` and `ros2 bag`

## Break it on purpose
- Trigger the E-stop during a motion command and verify that all joint commands halt safely; then test what happens if a controller fails to load.

## What I learned
<!-- Write your own notes here after finishing this project -->
