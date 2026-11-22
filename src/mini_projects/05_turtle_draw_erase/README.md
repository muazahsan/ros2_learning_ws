# Mini Project 05: Two-Robot Writer & Eraser (`turtle_draw_erase`)

A two-robot ROS 2 Humble project in `turtlesim`: type any letter (`A`–`Z`) or digit (`0`–`9`) in the terminal — **`turtle1` writes it** in bright yellow, and **`turtle2` chases behind and erases it** cleanly!

## ROS 2 Concepts Used
- **Producer–Consumer Architecture over Topics:**
  - `/writer_node` (`turtle1`) draws each stroke and publishes `(x, y, pen_down)` waypoints to `/erase_queue` (`geometry_msgs/msg/Point`).
  - `/eraser_node` (`turtle2`) subscribes to `/erase_queue`, buffers waypoints in a FIFO queue (`deque`), and replays them with a 1.2s delay.
- **Background-Matched Pen Erasing (`/turtle2/set_pen`):** `turtle2` paints over `turtle1`'s path using `turtlesim`'s exact background blue `RGB(69, 86, 255)` with width `12` (3× wider than `turtle1`'s width `4`).
- **Dynamic Spawning (`/spawn`):** `eraser_node` spawns `turtle2` automatically on startup.

## Build
```bash
cd ~/ros2_learning_ws
colcon build --packages-select turtle_draw_erase
source install/setup.bash
```

## Run (3 Terminals)

**Terminal 1 — Start `turtlesim`:**
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 — Start the Eraser (`turtle2`):**
```bash
source ~/ros2_learning_ws/install/setup.bash
ros2 run turtle_draw_erase eraser_node
```

**Terminal 3 — Start the Writer (`turtle1`) and type letters:**
```bash
source ~/ros2_learning_ws/install/setup.bash
ros2 run turtle_draw_erase writer_node
```
Type any letter (`A`–`Z`) or digit (`0`–`9`) and press **Enter**!
