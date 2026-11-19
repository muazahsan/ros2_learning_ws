# ROS 2 Humble Official-Aligned Learning Plan

Based on the official ROS 2 Humble documentation:
- Tutorials: https://docs.ros.org/en/humble/Tutorials.html
- Concepts: https://docs.ros.org/en/humble/Concepts.html

## Phase 1: Beginner — CLI Tools (No Code, Pure ROS 2 Concepts)
- **1.1** Configuring environment + `turtlesim` & `rqt`
- **1.2** Understanding **Nodes** (`ros2 node list`, `info`, remapping)
- **1.3** Understanding **Topics** (`ros2 topic list`, `echo`, `info`, `pub`, `hz`, `rqt_graph`)
- **1.4** Understanding **Services** (`ros2 service list`, `type`, `call`)
- **1.5** Understanding **Parameters** (`ros2 param list`, `get`, `set`, `dump`, `load`)
- **1.6** Understanding **Actions** (`ros2 action list`, `info`, `send_goal`)
- **1.7** Viewing logs (`rqt_console`), launching (`ros2 launch`), and recording (`ros2 bag`)

## Phase 2: Beginner — Client Libraries (Python `rclpy`)
- **2.1** Workspaces, `colcon`, and creating a Python package
- **2.2** Writing a simple **Publisher & Subscriber** (`02_temp_sensor_pubsub`)
- **2.3** Writing a simple **Service & Client** (`03_fan_service`)
- **2.4** Creating & using **Custom `.msg` and `.srv`** interfaces (`07_custom_messages`)
- **2.5** Using **Parameters** inside a Python node class (`05_parameters`)
- **2.6** Debugging setup with `ros2doctor`

## Phase 3: Intermediate
- **3.1** Writing a Python **Action Server & Client** (`04_countdown_action`)
- **3.2** Writing **Launch Files** (`06_launch_files`)
- **3.3** **Quality of Service (QoS)** profiles (`10_qos`)
- **3.4** **`tf2`** coordinate frames (`08_tf2_two_link`)
- **3.5** **URDF / Xacro** & visualizing in **RViz2** (`09_urdf_rviz`)

## Phase 4: Robotics Simulation & Control
- **4.1** **Gazebo** simulation (`12_gazebo_robot`)
- **4.2** **`ros2_control`** with mock hardware (`13_ros2_control_mock`)
- **4.3** **MoveIt 2** motion planning (`14_moveit`)
- **4.4** **Final Project:** SCARA Digital Twin + E-Stop (`15_final_scara_twin`)
