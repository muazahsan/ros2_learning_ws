# Mini Project 08: Autonomous Obstacle Avoidance (`turtle_apf_nav`)

An autonomous **Artificial Potential Fields (APF)** obstacle-avoidance system in ROS 2 Humble (`turtlesim`), featuring a **single-command Launch File**, **live-tunable ROS 2 Parameters**, and **real-time telemetry**.

## ROS 2 Concepts Used
- **ROS 2 Python Launch File (`launch/apf_nav.launch.py`):** Starts `turtlesim_node` (dark slate theme), `obstacle_manager`, and `apf_navigator` together in **1 command**.
- **Live Dynamic Parameters (`add_on_set_parameters_callback`):** Tune `max_speed`, `attraction_gain`, `repulsion_gain`, and `repulsion_radius` live while the robot is moving without restarting!
- **Artificial Potential Fields (APF) + Local-Minimum Escape:** Combines goal attraction, Khatib inverse-square obstacle repulsion, and a 25% tangential swirl vector so the robot smoothly weaves around all 5 obstacles without getting trapped.
- **Telemetry Topic (`/apf/status`):** Streams live distance-to-goal and nearest-obstacle clearance.

## Build
```bash
cd ~/ros2_learning_ws
colcon build --packages-select turtle_apf_nav
source install/setup.bash
```

## Run (Just 1 Terminal!)
```bash
source ~/ros2_learning_ws/install/setup.bash
ros2 launch turtle_apf_nav apf_nav.launch.py
```

## Tune Parameters Live (Optional Terminal 2)
```bash
# Make the robot take wider safety arcs around obstacles:
ros2 param set /apf_navigator repulsion_radius 3.0

# Speed up the robot live:
ros2 param set /apf_navigator max_speed 4.0

# Watch live distance & obstacle clearance telemetry:
ros2 topic echo /apf/status
```
