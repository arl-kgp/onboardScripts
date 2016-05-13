#!/bin/sh

sudo -E apt-get update  &&
sudo -E apt-get install screen python-wxgtk2.8 python-serial python-pyparsing python-matplotlib python-opencv python-pip python-numpy python-dev libxml2-dev libxslt-dev &&
sudo -E pip install pymavlink &&
sudo -E pip install mavproxy &&
sudo -E pip install dronekit &&
sudo -E pip install dronekit-sitl -UI &&
sudo -E pip install Flask