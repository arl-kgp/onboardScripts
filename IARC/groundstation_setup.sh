#!/bin/bash

sudo apt-get install libglew-dev &&
sudo apt-get install cmake &&
sudo apt-get install libboost-dev libboost-thread-dev libboost-filesystem-dev &&
sudo apt-get install libpython2.7-dev &&

cd ~/Downloads &&
mkdir -p ARK &&
cd ARK &&
git clone https://github.com/quadrotor-IITKgp/Pangolin.git || true &&
cd Pangolin &&
mkdir -p build &&
cd build &&
cmake -DCPP11_NO_BOOST=1 .. &&
make -j &&

cd ~/Downloads/ARK &&
hg clone https://bitbucket.org/eigen/eigen/ || true &&
hg up 3.1.0 &&
mkdir -p build &&
cd build &&
cmake .. &&
sudo make install &&

sudo apt-get install libblas-dev &&
sudo apt-get install liblapack-dev &&
sudo apt-get install screen &&

cd ~/Downloads/ARK &&
git clone https://github.com/quadrotor-IITKgp/ORB_SLAM2.git || true &&
cd ORB_SLAM2 &&
chmod +x build.sh &&
./build.sh &&
export ROS_PACKAGE_PATH=${ROS_PACKAGE_PATH}:$HOME/Downloads/ARK/ORB_SLAM2/Examples/ROS &&
echo "export ROS_PACKAGE_PATH=${ROS_PACKAGE_PATH}:$HOME/Downloads/ARK/ORB_SLAM2/Examples/ROS" >> ~/.bashrc &&
cd Examples/ROS/ORB_SLAM2 &&
mkdir -p build &&
cd build &&
cmake .. -DROS_BUILD_TYPE=Release &&
make -j &&

cd ~/catkin_ws &&
cd src &&
git clone https://github.com/quadrotor-IITKgp/ark_msgs.git || true &&
git clone https://github.com/quadrotor-IITKgp/ark_controls.git || true &&
git clone https://github.com/quadrotor-IITKgp/ark_stateestimation.git || true &&
git clone https://github.com/quadrotor-IITKgp/ark_runs.git || true &&
git clone https://github.com/quadrotor-IITKgp/onboardScripts.git || true &&

cd ~/catkin_ws &&
catkin_make --pkg ark_msgs
catkin_make

