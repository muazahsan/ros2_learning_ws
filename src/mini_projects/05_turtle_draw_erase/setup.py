from setuptools import find_packages, setup

package_name = 'turtle_draw_erase'

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
    description='Two-robot ROS 2 turtlesim project: turtle1 draws a letter and turtle2 erases it',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'writer_node = turtle_draw_erase.writer_node:main',
            'eraser_node = turtle_draw_erase.eraser_node:main',
        ],
    },
)
