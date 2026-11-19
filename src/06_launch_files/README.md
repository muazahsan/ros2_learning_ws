# 06_launch_files

## Goal
Write a Python launch file to start multiple nodes at once.
Pass parameters and remap topic names from the launch file.

## Concepts to learn
- ROS 2 Python launch files (`launch`, `launch_ros`)
- Starting multiple nodes with one command
- Topic remapping and parameter loading

## Task checklist
- [ ] Create a `launch/` folder and update `setup.py`
- [ ] Write a launch file for publisher and subscriber
- [ ] Add topic remapping in the launch file
- [ ] Run with `ros2 launch` and verify with `rqt_graph`

## Break it on purpose
- Remove the launch folder installation entry from `setup.py`, rebuild, and see why `ros2 launch` cannot find the file.

## What I learned
<!-- Write your own notes here after finishing this project -->
