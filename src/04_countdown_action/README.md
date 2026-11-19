# 04_countdown_action

## Goal
Build a ROS 2 action server that counts down from a target number.
Send feedback each second and support canceling the countdown.

## Concepts to learn
- Long-running tasks with Actions (Goal, Feedback, Result)
- Action server and client in `rclpy`
- Handling goal cancellation

## Task checklist
- [ ] Write a countdown action server
- [ ] Send a goal using `ros2 action send_goal --feedback`
- [ ] Write a Python action client
- [ ] Test canceling a goal mid-countdown

## Break it on purpose
- Send a negative number or zero as the countdown target without validation and see how the action server fails.

## What I learned
<!-- Write your own notes here after finishing this project -->
