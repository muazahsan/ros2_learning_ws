from setuptools import find_packages, setup

package_name = 'turtle_swarm'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='muaz',
    maintainer_email='muaz@example.com',
    description='Multi-robot leader-follower convoy swarm in ROS 2 turtlesim',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'swarm_controller = turtle_swarm.swarm_controller:main',
            'leader_pilot = turtle_swarm.leader_pilot:main',
        ],
    },
)
