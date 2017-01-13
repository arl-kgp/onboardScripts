#!/bin/sh

sudo -E apt-get update  &&
sudo -E apt-get install screen python-wxgtk3.0 python-serial python-pyparsing python-matplotlib python-opencv python-pip python-numpy python-dev libxml2-dev libxslt-dev &&
sudo -E pip install pymavlink==2.0.6 &&
sudo -E pip install mavproxy==1.5.0 &&
sudo -E pip install dronekit==2.9.0 &&
sudo -E pip install dronekit-sitl==3.2.0 -UI &&
sudo -E pip install Flask