from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math
import argparse

P1 = [22.32890386, 87.32263576, 2]
P2 = [22.32884598, 87.3224447, 2]

gps_points = [P1, P2]


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


def main(): 
    arm_and_takeoff(2)

    print "Set default/target airspeed to 1"
    vehicle.airspeed = 1

    for gps_point in gps_points:
        print "Going towards next point (groundspeed set to 1 m/s) ..."
        point1 = LocationGlobalRelative(gps_point[0], gps_point[1], gps_point[2])
        vehicle.simple_goto(point1, groundspeed=1)
        # printing the distance to go in meters
        while measure(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, gps_point[0], gps_point[1])>1 :
            print measure(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, gps_point[0], gps_point[1])
            time.sleep(3)
        print "reached point"

    print "landing"
    vehicle.mode = VehicleMode("LAND")

    # Close vehicle object before exiting script
    print "Close vehicle object"
    vehicle.close()

    # Shut down simulator if it was started.
    if sitl is not None:
        sitl.stop()

main()
