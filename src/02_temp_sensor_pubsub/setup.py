from setuptools import find_packages, setup

package_name = 'temp_sensor_pubsub'

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
    description='Minimal temperature sensor publisher and subscriber',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            # Format: 'command_name = package.file:function'
            'temp_publisher = temp_sensor_pubsub.temp_publisher:main',
            'temp_subscriber = temp_sensor_pubsub.temp_subscriber:main',
        ],
    },
)
