from dronekit import connect
from time import sleep
import argparse
import json

parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

#Start SITL if no connection string specified
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

# Connect to the Vehicle.
# print "Connecting to vehicle on: '/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Mega_2560_740313032373515082D1-if00'"
# vehicle = connect('/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Mega_2560_740313032373515082D1-if00', wait_ready=True, baud = 115200)

#print "Connecting to vehicle on: '/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Mega_2560_740313032373515082D1-if00'"
#vehicle = connect('192.168.43.57:14550',wait_ready=True)

fo = open("data/flight_data.txt", "w+")

while True:
    # Get some vehicle attributes (state)
    data = {}
    data["roll"] = vehicle.attitude.roll
    data["pitch"] = vehicle.attitude.pitch
    data["heading"] = vehicle.heading
    data["vario"] = 0
    data["speed"] = vehicle.groundspeed / 100
    data["altitude"] = vehicle.location.global_relative_frame.alt

    fo.write(json.dumps(data))
    sleep(1)

# Close vehicle object before exiting script
vehicle.close()
fo.close()

print("Completed")
