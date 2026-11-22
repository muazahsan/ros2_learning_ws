# Mini Project 04: Shape-Shifting Multi-Robot Swarm (`turtle_formation`)

A 5-robot ROS 2 Humble formation swarm in `turtlesim` that flies in rigid geometric formations and **morphs live** between **V-Formation → Diamond → Wing Line → Orbiting Circle**.

## ROS 2 Concepts Used
- **2D Coordinate Frame Transforms:** Converts each follower's local `(x, y)` offset in the leader's body frame into world coordinates using a 2D rotation matrix (`cos θ`, `sin θ`) — the mathematical foundation of ROS 2 `tf2`.
- **Live Topic Mode Switching:** Subscribes to `/swarm/formation` (`std_msgs/msg/String`) to morph the entire swarm on the fly.
- **Multi-Robot Namespacing + Collision Separation:** Dynamically spawns `turtle2`–`turtle5`, assigns neon trails via `/<name>/set_pen`, and applies inter-robot separation repulsion during shape transitions.

## Build
```bash
cd ~/ros2_learning_ws
colcon build --packages-select turtle_formation
source install/setup.bash
```

## Run (3 Terminals)

**Terminal 1 — Start `turtlesim`:**
```bash
ros2 run turtlesim turtlesim_node
```

**Terminal 2 — Start the Formation Controller (spawns 4 followers in V-formation):**
```bash
source ~/ros2_learning_ws/install/setup.bash
ros2 run turtle_formation formation_controller
```

**Terminal 3 — Start the Commander (flies leader loop + auto-morphs every 8s):**
```bash
source ~/ros2_learning_ws/install/setup.bash
ros2 run turtle_formation formation_commander
```

## Manual Live Morphing (Optional Terminal 4)
Switch shapes anytime from the CLI:
```bash
ros2 topic pub --once /swarm/formation std_msgs/msg/String "{data: 'v'}"
ros2 topic pub --once /swarm/formation std_msgs/msg/String "{data: 'diamond'}"
ros2 topic pub --once /swarm/formation std_msgs/msg/String "{data: 'line'}"
ros2 topic pub --once /swarm/formation std_msgs/msg/String "{data: 'circle'}"
```
