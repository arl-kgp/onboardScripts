#!/bin/bash
screen -d -m -S uav
screen -S uav -p 0 -X stuff "source_ros\n export ROS_MASTER_URI=http://raspberrypi:11311/\n rosrun tf static_transform_publisher 0 0 0 0 0 0 1 base_link fcu 10\n "
screen -S uav -X screen 1
screen -S uav -p 1 -X stuff "source_ros\n export ROS_MASTER_URI=http://raspberrypi:11311/\n export_orb\n roslaunch ~/ark_simulation/sim_catkin_ws/src/roslaunchs/orb2.launch\n"
screen -S uav -X screen 2
screen -S uav -p 2 -X stuff "source_ros\n export ROS_MASTER_URI=http://raspberrypi:11311/\n rosrun ark_stateestimation sensor_fusion_node"
screen -S uav -X screen 3
screen -S uav -p 3 -X stuff "source_ros\n export ROS_MASTER_URI=http://raspberrypi:11311/\n rosrun ark_controls overrider\n"
screen -S uav -X screen 4
screen -S uav -p 4 -X stuff "source_ros\n export ROS_MASTER_URI=http://raspberrypi:11311/\n rosrun ark_controls ark_controls\n"

#screen -d -m -S uav
#screen -S uav -p 0 -X stuff "roslaunch mavros ark.launch\n"
#screen -S uav -X screen 1
#screen -S uav -p 1 -X stuff "roscd usb_cam\n cd launch\n ./setup_cam.sh\n roslaunch usb_cam ark2.launch\n"