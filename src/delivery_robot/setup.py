from setuptools import find_packages, setup

package_name = 'delivery_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ezz',
    maintainer_email='163548505+Ezzinhoooo@users.noreply.github.com',
    description='Autonomous delivery robot mission node for Nav2 (ROS 2 Jazzy)',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'hello_delivery = delivery_robot.hello_delivery:main',
            'go_to_goal = delivery_robot.go_to_goal:main',
            'delivery_mission = delivery_robot.delivery_mission:main',
        ],
    },
)
