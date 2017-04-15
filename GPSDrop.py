from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math
import argparse
import rospy
from std_msgs.msg import UInt16

P1 = [22.31793176,87.30432468, 2]
P2 = [22.31795785,87.30457318, 2]
P3 = [22.31809707,87.30461613,2]
P4 = [22.31895938,87.30262122,2]
P5 = [22.31887949,87.30283219,2]
P6 = [22.31892094,87.30295963,2]


gps_points = [P1, P2,P3 , P4,P5,P6]


# Set up option parsing to get connection string


parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

# Start SITL if no connection string specified
if not args.connect:
    print "Starting copter simulator (SITL)"
    from dronekit_sitl import SITL
    sitl = SITL()
    sitl.download('copter', '3.3', verbose=True)
    sitl_args = ['-I0', '--model', 'quad', '--home=-35.361361,149.165230,584,353']
    sitl.launch(sitl_args, await_ready=True, restart=True)
    connection_string = 'tcp:127.0.0.1:5760'


# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    # print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    # while not vehicle.is_armable:
    #    print " Waiting for vehicle to initialise..."
    #    time.sleep(1)

    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print "Reached target altitude"
            break
        time.sleep(1)


def measure(lat1, lon1, lat2, lon2):  # generally used geo measurement function
    R = 6378.137  # Radius of earth in KM
    dLat = (lat2 - lat1) * math.pi / 180
    dLon = (lon2 - lon1) * math.pi / 180
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d * 1000  # meters

def goto(gps_point):
	print "Set default/target airspeed to 1"
	vehicle.airspeed = 1

   	vehicle.mode = VehicleMode("GUIDED")
	print "Going towards next point (groundspeed set to 1 m/s) ..."
	point1 = LocationGlobalRelative(gps_point[0], gps_point[1], gps_point[2])
	vehicle.simple_goto(point1, groundspeed=1)
	dist = measure(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, gps_point[0], gps_point[1])
    # printing the distance to go in meters
	while dist>1 :
		print dist
		time.sleep(1)            
		dist = measure(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, gps_point[0], gps_point[1])
	print "reached point"

def drop():
	pub = rospy.Publisher('/servo',UInt16,queue_size=10)
	i = 0
	while i in range(3) :
		rospy.sleep(1000)
	pub.publish(0)
	while i in range(3) :
		rospy.sleep(1000)
	pub.publish(180)

def main(): 
    arm_and_takeoff(2)
	rospy.init_node('serial_node')
    goto(P1)
    print "Dropping"
    drop()
    goto(P2)
    print "Landing"
    vehicle.mode = VehicleMode("LAND")

    # Close vehicle object before exiting script
    print "Close vehicle object"
    vehicle.close()

    # Shut down simulator if it was started.
    if sitl is not None:
        sitl.stop()

main()
