# ROS 2 Humble Learning Rules — RULES.md

- Always use **ROS 2 Humble**, **Ubuntu 22.04**, and **Python (`rclpy`)** unless the user asks for C++.
- Never use ROS 1, Foxy, or Iron code or commands.
- Check the official ROS 2 Humble docs (`docs.ros.org/en/humble/`) when unsure. Do not guess APIs.
- Always give the exact commands: `colcon build`, `source`, and `ros2 run` / `ros2 launch`.
- Always show how to check the running system with `ros2 topic list`, `ros2 node list`, and `rqt_graph`.
- Keep code minimal and commented. No extra features.
- Explain in simple words, step by step, with a visual diagram/infographic.
- Always include a short hands-on exercise or quiz question to check understanding.
- Update existing files. Never create duplicate files for the same project.
- Before real hardware, test in simulation. Add a safety stop for any motor.
