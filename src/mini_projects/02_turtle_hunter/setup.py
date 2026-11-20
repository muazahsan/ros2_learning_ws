from setuptools import find_packages, setup

package_name = 'turtle_hunter'

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
    description='Multi-node ROS 2 turtlesim autonomous target hunter',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'target_spawner = turtle_hunter.target_spawner:main',
            'turtle_chaser = turtle_hunter.turtle_chaser:main',
        ],
    },
)
