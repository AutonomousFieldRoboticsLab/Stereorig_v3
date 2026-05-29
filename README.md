# Stereorig_v3
This repository contains the setup files and launch configuration for the Stereorig system.


## Jetson setup

Refer to the `Jetson_setup.pdf` for Jetson setup instructions.

## Clone the Repository

`git clone https://github.com/AutonomousFieldRoboticsLab/Stereorig_v3.git`

## Configure the Launch Script

For the secondary Jetson, update launch.sh to use the following ROS 2 launch command:

`ros2 launch ros2_bringup stereorig_2.launch.py namespace:="jetson_2"`

## Build the Docker Image
Build the Docker image from the repository directory:

`docker build -t abe .`

## Register the Systemd Service
To automatically start the Docker container on boot, register `docker-container.service` with systemd.

`sudo cp docker-container.service /etc/systemd/system/docker-container.service`


`sudo systemctl daemon-reload`

`sudo systemctl enable docker-container.service`

`sudo systemctl start docker-container.service`

## View Service logs

To monitor the service logs, run:

`journalctl -u docker-container.service -f`
