from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math
import argparse
import zmq
import sys
import socket
from threading import *

#P1 = [22.31890386, 87.30263576, 2]
#P2 = [22.31884598, 87.3024447, 2]
# Connect to the Vehicle

#gps_points = [P1, P2]
#gps_point = [22.31890386, 87.30263576]
#const_altitude = 2
connected = False
# Set up option parsing to get connection string
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
port = 8000
print (host)
print (port)
serversocket.bind((host, port))
class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        connected = True
        while 1:
            pos = self.sock.recv(1024)
            if pos[0] == 'A' or pos[0] == 'H':
                gps = pos[1:].split(',')
                GotoModeA(gps)
            elif pos[0] == 'B' :
				gps_points = pos[1:].split('B')
				GotoModeB(gps_points)
            else :
                ModeLand()
            self.sock.send(str(vehicle.location.global_relative_frame.lat)+','+str(vehicle.location.global_relative_frame.lon)+'\n')

def sent(clientsocket):
	while True:
		clientsocket.send(str(vehicle.location.global_relative_frame.lat)+','+str(vehicle.location.global_relative_frame.lon)+'\n')
		time.sleep(0.1)
        #print 'Sending !\n'

parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, wait_ready=True)
# Start SITL if no connection string specified
if not args.connect:
    print "Starting copter simulator (SITL)"
    from dronekit_sitl import SITL
    sitl = SITL()
    sitl.download('copter', '3.3', verbose=True)
    sitl_args = ['-I0', '--model', 'quad', '--home=-35.361361,149.165230,584,353']
    sitl.launch(sitl_args, await_ready=True, restart=True)
    connection_string = 'tcp:127.0.0.1:5760'


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
    while True :
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print "Reached target altitude"
            break
        time.sleep(1)


def measure(lat1, lon1, lat2, lon2):  # generally used geo measurement function
    R = 6378.137  # Radius of earth in KM
    lat2 = float(lat2)
    lon2 = float(lon2)
    dLat = (lat2 - lat1) * math.pi / 180
    dLon = (lon2 - lon1) * math.pi / 180
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d * 1000  # meters

def GotoModeA(gps_point):
    height = abs(vehicle.location.global_relative_frame.alt - float(gps_point[2]))
    dist = measure(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, gps_point[0], gps_point[1])
    print "Going towards next point (groundspeed set to 1 m/s) ..."
    while (dist > 1 or height > 0.3)  :
        point1 = LocationGlobalRelative(float(gps_point[0]), float(gps_point[1]), float(gps_point[2]))
        vehicle.simple_goto(point1, groundspeed=5) 
        # printing the distance to go in meters
        dist = measure(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, gps_point[0], gps_point[1])
	print dist
        time.sleep(1)


def GotoModeB(gps_points):
	for gps in gps_points:
		gps_point = gps.split(',')
		height = abs(vehicle.location.global_relative_frame.alt - float(gps_point[2]))
		dist = measure(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, gps_point[0], gps_point[1])
		print "Going towards next point (groundspeed set to 5 m/s) ..."
        while (dist > 1 or height > 0.3):
            point1 = LocationGlobalRelative(float(gps_point[0]), float(gps_point[1]), float(gps_point[2]))
            vehicle.simple_goto(point1, groundspeed=5) 
            # printing the distance to go in meters
            dist = measure(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, gps_point[0], gps_point[1])
            print dist
            time.sleep(1)

def ModeLand():
    print 'Landing'
    vehicle.mode = VehicleMode("LAND")
    connected = False

def main():
    arm_and_takeoff(2)
    serversocket.listen(5)
    print ('server started and listening')
    while not connected:
        clientsocket, address = serversocket.accept()
        client(clientsocket, address)
        Thread(target=sent,args=(clientsocket,)).start()
    print "Set default/target airspeed to 1"
    vehicle.airspeed = 1

    bool_reached = True
    while connected:
        #gps_point = getGPS()
        time.sleep(3)
			

    # Close vehicle object before exiting script
    print "Close vehicle object"
    vehicle.close()

    # Shut down simulator if it was started.
    #if sitl is not None:
    #    sitl.stop()

main()
