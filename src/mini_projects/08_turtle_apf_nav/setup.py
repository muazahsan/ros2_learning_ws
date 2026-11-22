import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'turtle_apf_nav'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='muaz',
    maintainer_email='muaz@example.com',
    description='Autonomous obstacle avoidance in ROS 2 turtlesim using Artificial Potential Fields, Launch Files, and live Parameters',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'obstacle_manager = turtle_apf_nav.obstacle_manager:main',
            'apf_navigator = turtle_apf_nav.apf_navigator:main',
        ],
    },
)
