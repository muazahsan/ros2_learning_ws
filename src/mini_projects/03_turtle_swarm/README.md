# Mini Project 03: Multi-Robot Swarm / Leader–Follower Convoy (`turtle_swarm`)

A multi-robot ROS 2 Humble project in `turtlesim` where **1 leader** (`turtle1`) leads **4 autonomous followers** (`turtle2`–`turtle5`) in a synchronized, collision-free convoy with neon trails.

## ROS 2 Concepts Used
- **Multi-Robot Namespacing:** Each robot has its own `/turtleN/pose`, `/turtleN/cmd_vel`, and `/turtleN/set_pen` interfaces.
- **Multi-Node Architecture:**
  - `/swarm_controller`: Spawns followers via `/spawn`, sets neon pen colors via `/<name>/set_pen`, and runs a 20 Hz closed-loop leader–follower controller.
  - `/leader_pilot`: Drives `turtle1` along a smooth parametric figure-8 (infinity) trajectory (can be swapped with `turtle_teleop_key` for manual driving).
- **Closed-Loop Distance-Keeping Control:** Each follower maintains a safe gap (`SAFE_DISTANCE = 1.0`) behind the robot directly ahead, using `atan2(sin, cos)` angle wrapping and `cos(angle_error)` velocity scaling.

## Build
```bash
cd ~/ros2_learning_ws
colcon build --packages-select turtle_swarm
source install/setup.bash
```

## Run (3 Terminals)

**Terminal 1 — Start `turtlesim`:**
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 — Start the Swarm Controller (spawns 4 followers):**
```bash
source ~/ros2_learning_ws/install/setup.bash
ros2 run turtle_swarm swarm_controller
```

**Terminal 3 — Drive the Leader (choose Option A or B):**

*Option A (Autonomous Figure-8 — best for demo video):*
```bash
source ~/ros2_learning_ws/install/setup.bash
ros2 run turtle_swarm leader_pilot
```

*Option B (Manual Keyboard Driving):*
```bash
ros2 run turtlesim turtle_teleop_key
```
