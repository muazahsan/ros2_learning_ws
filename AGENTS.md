# ROS 2 Humble Learning Workspace — AGENTS.md

## Profile
- **Background:** ECE graduate with robotics hardware experience, new to ROS 2.
- **Learning Style:** Learn by doing. Uses AI to write code, but must understand every file and line.
- **Communication:** Use simple words. Explain pure ROS 2 Humble concepts (from `docs.ros.org/en/humble/`, no MCU/Arduino analogies). Explain step by step, use visual infographics/diagrams, and give short exercises to check understanding.

## Project List
1. `01_cli_turtlesim`
2. `02_temp_sensor_pubsub`
3. `03_fan_service`
4. `04_countdown_action`
5. `05_parameters`
6. `06_launch_files`
7. `07_custom_messages`
8. `08_tf2_two_link`
9. `09_urdf_rviz`
10. `10_qos`
11. `11_rosbag`
12. `12_gazebo_robot`
13. `13_ros2_control_mock`
14. `14_moveit`
15. `15_final_scara_twin`

## Custom / Mini Projects Organization
- Any custom, bonus, or experimental project requested by the user outside the 15 curriculum projects MUST be placed in its own numbered, clearly labeled directory under `src/mini_projects/<NN>_<project_name>/` (for example, `src/mini_projects/01_turtle_char_drawer/`).
- Every mini-project directory must include a `README.md` with its ROS 2 concepts, build command, and run commands so it stays structured and reusable.
- Track completed mini-projects under the **Mini Projects** section in `PROGRESS.md`.

## Workflow
1. User says which project to start.
2. Assistant explains the concept in simple words with a visual diagram (infographic).
3. Assistant builds the minimal version step by step.
4. Assistant explains every file and important line.
5. Assistant gives the exact commands to run and what output to expect.
6. Assistant gives a short exercise to check understanding.
7. Assistant tells the user how to break it. User breaks it, assistant explains the error.
8. Update `PROGRESS.md`.
9. Commit completed project changes to git.
