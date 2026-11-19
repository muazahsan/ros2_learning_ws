# 10_qos

## Goal
Experiment with Quality of Service (QoS) profiles in ROS 2.
Compare Reliable vs Best Effort and Volatile vs Transient Local.

## Concepts to learn
- DDS Quality of Service (Reliability, Durability, History)
- Creating `QoSProfile` in `rclpy`
- Diagnosing QoS mismatches

## Task checklist
- [ ] Create a publisher with `BEST_EFFORT` reliability
- [ ] Create a subscriber with `RELIABLE` reliability
- [ ] Fix the QoS profile so messages flow
- [ ] Test `TRANSIENT_LOCAL` for late-joining subscribers

## Break it on purpose
- Intentionally pair a `BEST_EFFORT` publisher with a `RELIABLE` subscriber and diagnose the silent failure with `ros2 topic info -v`.

## What I learned
<!-- Write your own notes here after finishing this project -->
