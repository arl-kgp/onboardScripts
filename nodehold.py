from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse 

_land = False

#kp=0.3,ki=0.01,kd=0.2

def arm_and_takeoff(aTargetAltitude):
    global _land
   # print kp
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    '''while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)'''

        
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("ALT_HOLD")
    vehicle.armed=True 
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)
   
    print "Taking off!"
    
   # vehicle.mode = VehicleMode("STABILIZE")
    #vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:

        try:
            if _land==False:       
                setz = aTargetAltitude   
                currentz = vehicle.location.global_relative_frame.alt
                PIDx = 0
                PIDy = 0
                errorz = setz - currentz
                sum_errorx = 0
                prev_errorx = 0
                errorx = 0
                sum_errory = 0
                prev_errory = 0
                errory = 0
                vehicle.armed=True 
                #Break and return from function just below target altitude.        
                if abs(errorz)>setz*0.1:
                    if errorz<0 :
                        vehicle.channels.overrides['3'] = 1340
                    elif errorz>0 :
                        vehicle.channels.overrides['3'] = 1660
                else:
                    vehicle.channels.overrides['3'] = 1500
                    print "Reached target altitude"
                print " Altitude: ", currentz , "errorz:", errorz,"setz",setz
                print "throttle",vehicle.channels['3']
                PIDx = kpx*errorx + kix*sum_errorx + kdx*prev_errorx
                vehicle.channels.overrides['1'] = PIDx*100 + 1500  
                sum_errorx + sum_errorx + errorx
                prev_errorx = errorx
                print "xvel",vehicle.velocity[0],"xthrottle",vehicle.channels.overrides['1']   
                PIDy = kpy*errory + kiy*sum_errory + kdy*prev_errory
                vehicle.channels.overrides['2'] = PIDy*100 + 1500  
                sum_errory + sum_errory + errory
                prev_errory = errory
                print "yvel",vehicle.velocity[1],"ythrottle",vehicle.channels.overrides['2']   
                time.sleep(1)
            else:
                print "hi"
                vehicle.channels.overrides['3']=0
                exit()
             
        except KeyboardInterrupt:
            vehicle.channels.overrides['3']=0
           # vehicle.mode = VehicleMode("LAND")            
           # if _land:
            #    vehicle.channels.overrides['3']=1000
            #    exit()
            _land = True

#Set up option parsing to get connection string
 
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', 
                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


#connection_string = '/dev/serial/by-id/usb-Arduino__www.arduino.cc__Arduino_Mega_2560_740313032373515082D1-if00' #for serial
connection_string = 'udp:127.0.0.1:14550'

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % connection_string
vehicle = connect(connection_string, wait_ready=True)   #for udp
#vehicle = connect(connection_string, baud=115200, wait_ready=True)   #for serial
print "kpx,kix,kdx"
kpx = float(input())
kix = float(input())
kdx = float(input())
print "kpy,kiy,kdy"
kpy = float(input())
kiy = float(input())
kdy = float(input())

print _land

arm_and_takeoff(1)



#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()
