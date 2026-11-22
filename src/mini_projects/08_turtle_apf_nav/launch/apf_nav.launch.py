from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Launch turtlesim + obstacle_manager + apf_navigator in one command."""
    return LaunchDescription([
        # 1. Turtlesim simulator with dark slate background for high contrast
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim',
            parameters=[{
                'background_r': 20,
                'background_g': 28,
                'background_b': 48,
            }],
        ),
        # 2. Spawns 5 static obstacles and manages rotating corner goals
        Node(
            package='turtle_apf_nav',
            executable='obstacle_manager',
            name='obstacle_manager',
            output='screen',
        ),
        # 3. Artificial Potential Field navigator with live-tunable ROS 2 parameters
        Node(
            package='turtle_apf_nav',
            executable='apf_navigator',
            name='apf_navigator',
            output='screen',
            parameters=[{
                'max_speed': 2.6,
                'attraction_gain': 1.8,
                'repulsion_gain': 3.5,
                'repulsion_radius': 2.1,
            }],
        ),
    ])
