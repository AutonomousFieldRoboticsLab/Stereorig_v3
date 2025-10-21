# Stereorig_v3

## Git clone the repo inside stereorig primary/secondary modules
`cd /ws/src/`

`git clone https://github.com/AutonomousFieldRoboticsLab/Stereorig_v3.git .`

## Enter the Docker container
`docker --exec -it <container-name> /bin/bash`

## Source the .bashrc
`source ~/.bashrc`

## Source ros
`source /opt/ros/humble/setup.bash`

## Source workspace
`cd /ws`

`source install/local_setup.bash`

## Script to stop docker-container.service
### Primary 
`systemctl stop --user docker-container.service` 

### Secondary 
`systemctl stop docker-container.service`




