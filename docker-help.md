# Using Docker

Docker is a tool that runs and manages **containers**. A container is similar to a very lightweight virtual machine.

For this workshop, we start groups of containers all at once using a command called **docker-compose**. This allows us to run multiple ROS nodes in one go.

This repository contains 4 groups of containers, each one provides an entire ROS system with different settings:

* **ROS Basic**: a minimal ROS system containing just a master node and a few other nodes required to access it from Windows. [files](docker/ros-system/ros-basic).
* **ROS UR5 - Planning**: a ROS system configured with MoveIt! motion planning for a UR5 robot. [files](docker/ros-system/ros-ur5).
* **ROS ABB Linear axis - Planning**: a ROS system configured with MoveIt! motion planning for an ABB linear axis system. [files](docker/ros-system/ros-abb-linear-axis).
* **ROS ABB Linear axis - Execution**: a ROS system configured with MoveIt! motion planning for a ABB linear axis system and the ABB driver to execute trajectories on a real (or virtual) robot. [files](docker/ros-system/ros-abb-linear-axis).

## How to start docker containers

### From the command prompt

Open your Anaconda prompt (or the command prompt), go to the folder where the `docker-compose.yml` file resides, and run:

    docker-compose up -d

Once you're done with the system, you can remove all containers with:

    docker-compose down

### From Visual Studio Code

If you have the `Docker` extension installed, you can right-click any `docker-compose.yml` file and select `Compose Up` and `Compose Down` to turn the systems on and off.
