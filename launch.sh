#!/bin/bash
source /opt/ros/humble/setup.bash
source /ws/install/setup.bash
cd data
ros2 launch ros2_bringup stereorig_1.launch.py namespace:="jetson_1"
/bin/bash
