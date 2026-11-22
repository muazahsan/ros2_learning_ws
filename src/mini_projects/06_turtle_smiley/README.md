# Mini Project 06: Turtlesim Smiley Face Drawer (`turtle_smiley`)

A ROS 2 Humble node that draws a colorful **Smiley Face** in `turtlesim` using parametric circle & arc trajectories and smooth continuous waypoint tracking.

## ROS 2 Concepts Used
- **Parametric Trajectory Generation (`make_arc`):** Generates smooth `(x, y)` circle and arc waypoints (`face`, `left_eye`, `right_eye`, `smile`).
- **Topics:** Publishes `/turtle1/cmd_vel` (`geometry_msgs/Twist`) and subscribes to `/turtle1/pose` (`turtlesim/Pose`).
- **Services:** Calls `/clear` (`std_srvs/Empty`) and `/turtle1/set_pen` (`turtlesim/SetPen`) to switch colors and lift/lower the pen between features.

## Build
```bash
cd ~/ros2_learning_ws
colcon build --packages-select turtle_smiley
source install/setup.bash
```

## Run (2 Terminals)

**Terminal 1 — Start `turtlesim`:**
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 — Draw the Smiley Face:**
```bash
source ~/ros2_learning_ws/install/setup.bash
ros2 run turtle_smiley smiley_drawer
```
