# 12_gazebo_robot

## Goal
Spawn your URDF robot model inside Gazebo Classic.
Add physics properties (inertia, collision) and a simulated sensor or actuator.

## Concepts to learn
- URDF inertia and collision tags
- Spawning robots with `gazebo_ros`
- Bridging Gazebo simulation with ROS 2 topics

## Task checklist
- [ ] Add `<inertial>` and `<collision>` tags to the robot URDF
- [ ] Launch Gazebo with an empty world
- [ ] Spawn the robot into Gazebo
- [ ] Verify topics and TF in ROS 2

## Break it on purpose
- Set a link's mass or inertia to zero in URDF and observe what happens in Gazebo physics.

## What I learned
<!-- Write your own notes here after finishing this project -->
