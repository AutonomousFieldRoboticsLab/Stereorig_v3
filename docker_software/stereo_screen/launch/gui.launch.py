from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    cam_topic = LaunchConfiguration('cam_topic', default='debayer/image_raw/rgb')
    imu_topic = LaunchConfiguration("imu_topic", default="imu/data")
    depth_topic = LaunchConfiguration("depth_topic", default="bar30/depth")
    tag_topic = LaunchConfiguration("tag_topic", default="apriltag_detections")
    bag_topic = LaunchConfiguration("bag_topic", default="bag")
    sonar_topic = LaunchConfiguration("sonar_topic", default="imagenex831l/sonar_health")
    device = LaunchConfiguration('device', default="")

    return LaunchDescription([
        Node(
            package='custom_guyi',
            executable='custom_guyi',
            name='custom_guyi',
            output='screen',
            parameters=[{'cam_topic': cam_topic, 'device' : device, 'imu_topic' : imu_topic, 'depth_topic' : depth_topic, 'sonar_topic' : sonar_topic, 'tag_topic': tag_topic, 'bag_topic': bag_topic}]
        )
    ])
