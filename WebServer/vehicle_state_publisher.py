from dronekit import connect
import time
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


while True:
    # Get some vehicle attributes (state)
    fo = open("data/flight_data.txt", "w")
    data = {}
    data["roll"] = vehicle.attitude.roll*180/3.14
    data["pitch"] = vehicle.attitude.pitch*180/3.14
    data["heading"] = vehicle.heading
    data["vario"] = 0
    data["speed"] = vehicle.groundspeed / 100
    alt = vehicle.location.global_relative_frame.alt*1000
    if alt < 0:
        data["altitude"] = 0
    else:
        data["altitude"] = vehicle.location.global_relative_frame.alt*1000

    fo.write(json.dumps(data))
    fo.close()
    time.sleep(100.0 / 1000.0)

# Close vehicle object before exiting script
vehicle.close()
fo.close()

print("Completed")
