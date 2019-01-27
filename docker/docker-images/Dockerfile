# Container for robotic assembly packages (ABB & UR)
#
# Build:
#  docker build --rm -f "docker\docker-images\Dockerfile" -t gramaziokohler/robotic-assembly:workshop-19.01 docker\docker-images
#
# Usage:
#  docker pull gramaziokohler/robotic-assembly:workshop-19.01

FROM moveit/moveit:kinetic-release
LABEL maintainer "Gonzalo Casas <casas@arch.ethz.ch>"

SHELL ["/bin/bash","-c"]

# Install packages
RUN apt-get update && apt-get install -y \
    # Basic utilities
    iputils-ping \
    # ROS bridge server and related packages
    ros-${ROS_DISTRO}-rosbridge-server \
    ros-${ROS_DISTRO}-tf2-web-republisher \
    --no-install-recommends \
    # Clear apt-cache to reduce image size
    && rm -rf /var/lib/apt/lists/*

# Create local catkin workspace
ENV CATKIN_WS=/root/catkin_ws
ADD robotic_setups.tar.gz $CATKIN_WS/src
WORKDIR $CATKIN_WS/src

RUN source /opt/ros/${ROS_DISTRO}/setup.bash \
    # Update apt-get because its cache is always cleared after installs to keep image size down
    && apt-get update \
    # ROS File Server
    && git clone https://github.com/gramaziokohler/ros_file_server.git \
    # ABB packages
    && git clone -b ${ROS_DISTRO}-devel https://github.com/ros-industrial/abb.git \
    && git clone -b ${ROS_DISTRO}-devel https://github.com/ros-industrial/abb_experimental.git \
    # UR packages
    && git clone -b ${ROS_DISTRO}-devel https://github.com/ros-industrial/universal_robot.git \
    && git clone -b ${ROS_DISTRO}-devel https://github.com/ros-industrial/ur_modern_driver \
    # Install dependencies
    && cd $CATKIN_WS \
    && rosdep install -y --from-paths . --ignore-src --rosdistro ${ROS_DISTRO} \
    # Build catkin workspace
    && catkin_make

COPY ./ros_catkin_entrypoint.sh /

ENTRYPOINT ["/ros_catkin_entrypoint.sh"]
CMD ["bash"]

