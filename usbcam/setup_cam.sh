#!/bin/sh

CAMERA=/dev/video0 &&
EXPOSURE=0 &&
v4l2-ctl -d $CAMERA -c white_balance_temperature_auto=0 &&
v4l2-ctl -d $CAMERA -c backlight_compensation=0 &&
v4l2-ctl -d $CAMERA -c exposure_auto=3 &&
#v4l2-ctl -d $CAMERA -c exposure_absolute=$EXPOSURE &&
v4l2-ctl -d $CAMERA -c exposure_auto_priority=1 &&
v4l2-ctl -d $CAMERA -c focus_auto=0 &&
v4l2-ctl -d $CAMERA -c focus_absolute=0

