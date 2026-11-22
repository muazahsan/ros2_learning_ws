# Mini Project 07: Turtlesim Iron Man Helmet (`turtle_ironman`)

A ROS 2 Humble node that autonomously draws **Iron Man's Red & Gold Helmet** with glowing cyan eyes in `turtlesim` using layered symmetric waypoint trajectories and crisp turn-then-drive control.

## ROS 2 Concepts Used
- **Layered Multi-Color Waypoint Plotting:** Draws 12 symmetric layers (red helmet silhouette, gold faceplate with forehead notch, dark armor panel lines, and glowing cyan + white eyes).
- **Sharp Corner Turn-Then-Drive Control:** Rotates in place before driving straight on every vertex so armor edges stay razor-sharp.
- **ROS 2 Topics + Services:** Uses `/turtle1/cmd_vel`, `/turtle1/pose`, `/turtle1/set_pen`, and `/clear`.

## Build
```bash
cd ~/ros2_learning_ws
colcon build --packages-select turtle_ironman
source install/setup.bash
```

## Run (2 Terminals)

**Terminal 1 — Start `turtlesim`:**
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 — Draw Iron Man:**
```bash
source ~/ros2_learning_ws/install/setup.bash
ros2 run turtle_ironman ironman_drawer
```
