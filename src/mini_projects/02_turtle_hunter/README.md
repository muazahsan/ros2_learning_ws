# 02 — Autonomous Turtle Hunter (`turtle_hunter`)

A multi-node ROS 2 Humble mini-project in `turtlesim`: a spawner node creates random target turtles, and an autonomous chaser node tracks and catches them using closed-loop proportional control with colorful pursuit trails.

## ROS 2 Concepts Used
- **Multi-Node Architecture:**
  - `/target_spawner` — manages targets via `/spawn` and `/kill`, tracks score, and publishes `/hunter/target_pose`
  - `/turtle_chaser` — subscribes to `/turtle1/pose` and `/hunter/target_pose`, drives `turtle1` via `/turtle1/cmd_vel`, and notifies `/hunter/target_caught`
- **Topics:** `/turtle1/cmd_vel`, `/turtle1/pose`, `/hunter/target_pose`, `/hunter/target_caught`
- **Services:** `/spawn`, `/kill`, `/turtle1/set_pen`
- **Control Logic:** 20 Hz closed-loop proportional pursuit with `atan2(sin, cos)` angle wrapping and `cos(angle_error)` velocity scaling

## Build
```bash
cd ~/ros2_learning_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select turtle_hunter
```

## Run
Open **3 terminals**:

**Terminal 1 (`turtlesim`):**
```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 (`target_spawner`):**
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_learning_ws/install/setup.bash
ros2 run turtle_hunter target_spawner
```

**Terminal 3 (`turtle_chaser`):**
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_learning_ws/install/setup.bash
ros2 run turtle_hunter turtle_chaser
```
