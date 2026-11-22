from setuptools import find_packages, setup

package_name = 'turtle_smiley'

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
    description='ROS 2 turtlesim node that draws a colorful smiley face using smooth arc trajectories',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'smiley_drawer = turtle_smiley.smiley_drawer:main',
        ],
    },
)
