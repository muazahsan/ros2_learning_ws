from setuptools import find_packages, setup

package_name = 'turtle_formation'

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
    description='Shape-shifting multi-robot formation swarm in ROS 2 turtlesim',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'formation_controller = turtle_formation.formation_controller:main',
            'formation_commander = turtle_formation.formation_commander:main',
        ],
    },
)
