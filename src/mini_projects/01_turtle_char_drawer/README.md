# 01 — Turtlesim Character Drawer (`turtle_char_drawer`)

An interactive ROS 2 Humble mini-project: type any letter (`A`–`Z`) or number (`0`–`9`) in the terminal, and `turtle1` drives around in `turtlesim` to draw it.

## ROS 2 Concepts Used
- **Publisher:** `/turtle1/cmd_vel` (`geometry_msgs/msg/Twist`) — drives and turns the turtle
- **Subscriber:** `/turtle1/pose` (`turtlesim/msg/Pose`) — reads live `(x, y, theta)` position
- **Service Client:** `/turtle1/set_pen` (`turtlesim/srv/SetPen`) — lifts/lowers the pen between strokes
- **Service Client:** `/clear` (`std_srvs/srv/Empty`) — clears the screen before each new character

## Build
```bash
cd ~/ros2_learning_ws
source /opt/ros/humble/setup.bash
colcon build --packages-select turtle_char_drawer
```

## Run
**Terminal 1 (turtlesim):**
```bash
source /opt/ros/humble/setup.bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 (character drawer):**
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_learning_ws/install/setup.bash
ros2 run turtle_char_drawer char_drawer
```
