FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
ENV ROS_DISTRO=humble

RUN apt-get update && apt-get install -y locales &&\
    locale-gen en_US en_US.UTF-8 &&\
    update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

RUN apt-get install -y software-properties-common &&\
    add-apt-repository universe

RUN apt-get update && apt-get install -y \
    cmake \
    zip \
    unzip \
    git \
    tmux \
    wget \
    curl \
    vim \
    python3-smbus2 \
    i2c-tools \
    build-essential \
    libgeographic-dev \
    geographiclib-tools && \
    rm -rf /var/lib/apt/lists/*

RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release; echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

RUN apt-get update && apt-get install -y \
    python3-flake8-docstrings \
    python3-pip \
    python3-pytest-cov \
    python3-flake8-blind-except \
    python3-flake8-builtins \
    python3-flake8-class-newline \
    python3-flake8-comprehensions \
    python3-flake8-deprecated \
    python3-flake8-import-order \
    python3-flake8-quotes \
    python3-pytest-repeat \
    python3-pytest-rerunfailures \
    libasio-dev \
    ros-humble-ros-core \
    ros-humble-rqt-graph \
    ros-humble-rosbag2 \
    ros-humble-ros2bag \
    ros-humble-ament-cmake-clang-format \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-pykdl \
    python3-vcstool \
    python3-numpy \
    python3-transforms3d &&\
    apt-get -y autoremove &&\
    rm -rf /var/lib/apt/lists/*

RUN rosdep init && rosdep update

RUN apt-get update && apt-get install -y \
    python3-pytest-timeout

RUN mkdir -p /opt/ros2_ws/src && \
    cd /opt/ros2_ws && \
    vcs import src --input https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos && \
    /bin/bash -c '. /opt/ros/humble/setup.bash && rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers"'

RUN mkdir -p /ws/src

COPY docker_software/ /ws/src

RUN mkdir -p /tmp/ros_excluded && \
    for pkg in ros2_bringup imagenex831l_ROS2 ros2_aruco; do \
        if [ -d "/ws/src/$pkg" ]; then \
            mv "/ws/src/$pkg" "/tmp/ros_excluded/$pkg"; \
        fi; \
    done

RUN apt-get install -y python3-opencv

WORKDIR /ws

RUN apt-get update && apt-get install -y \
	ros-humble-ament-cmake \
	ros-humble-control-msgs \
	iputils-ping \
	ros-humble-apriltag* \
	ros-humble-rclcpp* \
	ros-humble-nmea-msgs \
	ros-humble-rtcm-msgs \ 
	ros-humble-microstrain-inertial-driver \
	ros-humble-microstrain-inertial-msgs \
    ros-humble-rosbag2-py \
    ros-humble-rosbag2-storage-default-plugins \
    ros-humble-example-interfaces \ 
    qt5-qmake \ 
    libqt5core5a \
	libqt5quick5 \
	libqt5widgets5 \
	libqt5gui5 \
	qtbase5-dev \
	qtdeclarative5-dev \
	libqt5svg5-dev \
	ros-humble-rviz2 \
	ros-humble-rviz-common \
	ros-humble-rviz-default-plugins \
	ros-humble-rviz-rendering \
	libopencv-dev

RUN rosdep install --from-paths src --ignore-src -r -y

RUN echo 29

RUN for pkg in ros2_bringup imagenex831l_ROS2 ros2_aruco; do \
        if [ -d "/tmp/ros_excluded/$pkg" ]; then \
            mv "/tmp/ros_excluded/$pkg" "/ws/src/"; \
        fi; \
    done

RUN echo "source /opt/ros/humble/setup.bash" >> /etc/bash.bashrc

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    colcon build && \
    source install/setup.bash"

RUN echo '#!/bin/bash\nset -e\nsource "/opt/ros/humble/setup.bash"\nexec "$@"' > /ros_entrypoint.sh && \
    chmod +x /ros_entrypoint.sh

COPY launch.sh /launch.sh
RUN chmod +x /launch.sh

ENTRYPOINT ["/ros_entrypoint.sh"]

CMD ["/launch.sh"]
