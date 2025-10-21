# Custom_guyi

This ROS2 package controls the GUI that displays on the Jetson Orin screens on boot. The node subscribes to the following topics:
- **debayer/image_raw/rgb** - Camera
- **bar30/depth** - Depth sensor
- **imagenex831l/sonar_health** - Sonar
- **imu/data** - IMU

For the IMU and sonar, the GUI displays "active" or "not active" depending on whether the topics have a publisher. Similarly, the depth sensor will display "not active" if there is no publisher and the depth value if there is. The image from the image topic displays directly on the screen. The gui determines if the orin is connected by pinging the ip address of the other and waiting for a response. If there is no response the orin connection is not active, otherwise it is active.
