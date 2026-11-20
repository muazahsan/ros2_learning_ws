from setuptools import find_packages, setup

package_name = 'turtle_char_drawer'

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
    description='Interactive ROS 2 turtlesim character drawing game',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'char_drawer = turtle_char_drawer.char_drawer_node:main',
        ],
    },
)
