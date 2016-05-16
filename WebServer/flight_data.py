from dronekit import connect
from time import sleep
import argparse  

parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', 
                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect

# Connect to the Vehicle.
print "Connecting to vehicle on: '/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Mega_2560_740313032373515082D1-if00'"
vehicle = connect('/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Mega_2560_740313032373515082D1-if00', wait_ready=True, baud = 115200)

#print "Connecting to vehicle on: '/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Mega_2560_740313032373515082D1-if00'"
#vehicle = connect('192.168.43.57:14550',wait_ready=True)



while True:
    # Get some vehicle attributes (state)
    print "Global Location: %s" % vehicle.location.global_frame
    print "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
    print "Local Location: %s" % vehicle.location.local_frame    #NED
    print "Attitude: %s" % vehicle.attitude
    print "Velocity: %s" % vehicle.velocity
    print "GPS: %s" % vehicle.gps_0
    print "Groundspeed: %s" % vehicle.groundspeed
    print "Airspeed: %s" % vehicle.airspeed
    print "Gimbal status: %s" % vehicle.gimbal
    print "Battery: %s" % vehicle.battery
    print "EKF OK?: %s" % vehicle.ekf_ok
    print "Last Heartbeat: %s" % vehicle.last_heartbeat
    print "Rangefinder: %s" % vehicle.rangefinder
    print "Rangefinder distance: %s" % vehicle.rangefinder.distance
    print "Rangefinder voltage: %s" % vehicle.rangefinder.voltage
    print "Heading: %s" % vehicle.heading
    print "System status: %s" % vehicle.system_status.state
    print "Mode: %s" % vehicle.mode.name    # settable
    print "Armed: %s" % vehicle.armed    # settable
    sleep(0.1)
    print ""

# Close vehicle object before exiting script
vehicle.close()

print("Completed")

