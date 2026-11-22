# ROS 2 Humble Learning Progress

Status options: `Not started` / `In progress` / `Broke & fixed` / `Done`

## Phase 1: Beginner — CLI Tools
| Module | Topic | Status | Date | Notes |
|--------|-------|--------|------|-------|
| 1.1 | Environment + `turtlesim` & `rqt` | Done | 2026-11-19 | Ran turtlesim, teleop, spawned turtle2 |
| 1.2 | Understanding **Nodes** | Done | 2026-11-19 | Learned nodes, `ros2 node list/info`, and `--remap __node` |
| 1.3 | Understanding **Topics** | In progress | 2026-11-19 | |
| 1.4 | Understanding **Services** | Not started | - | |
| 1.5 | Understanding **Parameters** | Not started | - | |
| 1.6 | Understanding **Actions** | Not started | - | |
| 1.7 | `rqt_console`, `ros2 launch`, `ros2 bag` | Not started | - | |

## Phase 2: Beginner — Client Libraries (Python `rclpy`)
| Module | Topic | Status | Date | Notes |
|--------|-------|--------|------|-------|
| 2.1 | Workspaces, `colcon`, creating a package | Not started | - | |
| 2.2 | Publisher & Subscriber (`02_temp_sensor_pubsub`) | Not started | - | Package built, will review in Phase 2 |
| 2.3 | Service & Client (`03_fan_service`) | Not started | - | |
| 2.4 | Custom `.msg` / `.srv` (`07_custom_messages`) | Not started | - | |
| 2.5 | Parameters in Python (`05_parameters`) | Not started | - | |
| 2.6 | `ros2doctor` | Not started | - | |

## Phase 3: Intermediate
| Module | Topic | Status | Date | Notes |
|--------|-------|--------|------|-------|
| 3.1 | Action Server & Client (`04_countdown_action`) | Not started | - | |
| 3.2 | Launch Files (`06_launch_files`) | Not started | - | |
| 3.3 | Quality of Service (`10_qos`) | Not started | - | |
| 3.4 | `tf2` Coordinate Frames (`08_tf2_two_link`) | Not started | - | |
| 3.5 | URDF / Xacro + RViz2 (`09_urdf_rviz`) | Not started | - | |

## Phase 4: Simulation & Control
| Module | Topic | Status | Date | Notes |
|--------|-------|--------|------|-------|
| 4.1 | Gazebo Simulation (`12_gazebo_robot`) | Not started | - | |
| 4.2 | `ros2_control` Mock (`13_ros2_control_mock`) | Not started | - | |
| 4.3 | MoveIt 2 (`14_moveit`) | Not started | - | |
| 4.4 | Final SCARA Digital Twin (`15_final_scara_twin`) | Not started | - | |

## Mini Projects (`src/mini_projects/`)
| # | Project | Package | Status | Date | Notes |
|---|---------|---------|--------|------|-------|
| 01 | Turtlesim Character Drawer | `turtle_char_drawer` | Done | 2026-11-20 | Draws A-Z and 0-9 in turtlesim from terminal input using Topics + Services |
| 02 | Autonomous Turtle Hunter | `turtle_hunter` | Done | 2026-11-20 | Multi-node target spawner + closed-loop proportional chaser in turtlesim |
| 03 | Multi-Robot Swarm Convoy | `turtle_swarm` | Done | 2026-11-21 | 5-robot leader-follower convoy with safe-gap control & autonomous figure-8 leader |
| 04 | Shape-Shifting Formation Swarm | `turtle_formation` | Done | 2026-11-21 | 5-robot swarm using 2D frame transforms to morph live (V / Diamond / Line / Circle) |
| 05 | Two-Robot Writer & Eraser | `turtle_draw_erase` | Done | 2026-11-22 | Producer-consumer multi-robot nodes: turtle1 draws A-Z/0-9 and turtle2 erases it |
| 06 | Turtlesim Smiley Face | `turtle_smiley` | Done | 2026-11-22 | Draws a colorful smiley face using parametric circle/arc waypoint trajectories |
| 07 | Turtlesim Iron Man Helmet | `turtle_ironman` | Done | 2026-11-22 | Draws Iron Man's red-and-gold helmet with glowing cyan eyes using layered waypoints |
| 08 | APF Obstacle Avoidance | `turtle_apf_nav` | Done | 2026-11-22 | Artificial Potential Fields obstacle avoidance with ROS 2 Launch File & live Parameters |
