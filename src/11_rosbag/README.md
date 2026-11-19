# 11_rosbag

## Goal
Record live ROS 2 topic data to a bag file and play it back.
Inspect recorded messages without running the original sensor node.

## Concepts to learn
- Recording data with `ros2 bag record`
- Inspecting bags with `ros2 bag info`
- Replaying data with `ros2 bag play`

## Task checklist
- [ ] Run a publisher node and record its topic
- [ ] Inspect the recorded bag metadata
- [ ] Stop the publisher and replay the bag
- [ ] Verify a subscriber receives the replayed data

## Break it on purpose
- Record with a wrong topic name (or no active publisher) and inspect the empty bag with `ros2 bag info`.

## What I learned
<!-- Write your own notes here after finishing this project -->
