# 08_tf2_two_link

## Goal
Broadcast coordinate frames for a simple 2-link robotic arm using `tf2`.
Listen to the transform between the base frame and the end-effector.

## Concepts to learn
- Coordinate frames and transforms (`tf2_ros`)
- Static vs dynamic transform broadcasters
- Inspecting TF trees with `view_frames` and RViz2

## Task checklist
- [ ] Write a broadcaster for base -> link1 -> link2
- [ ] Write a TF2 listener to compute end-effector pose
- [ ] Inspect transforms with `ros2 run tf2_ros tf2_echo`
- [ ] Visualize frames in RViz2

## Break it on purpose
- Publish two frames with no parent-child connection (disconnected TF tree) and observe the TF2 lookup error.

## What I learned
<!-- Write your own notes here after finishing this project -->
