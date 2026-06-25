import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    aruco_params = os.path.join(
        get_package_share_directory('ros2_aruco'),
        'config',
        'aruco_parameters.yaml'
        )

    # device = LaunchConfiguration('device')
    image_topic = LaunchConfiguration('image_topic')
    camera_info_topic = LaunchConfiguration('camera_info_topic')
    aruco_dictionary_id = LaunchConfiguration('aruco_dictionary_id')

    aruco_node = Node(
        package='ros2_aruco',
        executable='aruco_node',
        parameters=[
            aruco_params,
            {
                # 'device': device,
                'image_topic': image_topic,
                'camera_info_topic': camera_info_topic,
                'aruco_dictionary_id': aruco_dictionary_id
            },
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument('device', default_value=''),
        DeclareLaunchArgument('aruco_dictionary_id', default_value='DICT_ARUCO_ORIGINAL'),
        DeclareLaunchArgument('image_topic', default_value='flir_camera/image_raw'),
        DeclareLaunchArgument('camera_info_topic', default_value='flir_camera/camera_info'),
        aruco_node
    ])
