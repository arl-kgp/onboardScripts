import cv2
import numpy as np
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse 

#Global Variables
#TODO: Remove them from global
_land = False
fx = fy = 0
group_distance = 500
vehicle = None

def arrange_points(pt1, pt2):
    p1 = p2 = 0
    pt1x, pt1y = pt1
    pt2x, pt2y = pt2
    if pt1x == 0:
        p1 = 1
    if pt1x == fx:
        p1 = 3
    if pt2x == 0:
        p2 = 1
    if pt2x == fx:
        p2 = 3
    if pt1y == 0:
        p1 = 2
    if pt1y == fy:
        p1 = 4
    if pt2y == 0:
        p2 = 2
    if pt2y == fy:
        p2 = 4
    if p1 > p2:
        x = pt1
        pt1 = pt2
        pt2 = x
    return (pt1x, pt1y)

# Function to find line points
def line_points(line):
    rho, theta = line
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    pt1x = np.round(x0 + 1000 * (-b))
    pt1y = np.round(y0 + 1000 * (a))
    pt2x = np.round(x0 - 1000 * (-b))
    pt2y = np.round(y0 - 1000 * (a))

    if pt2x == pt1x:
        if pt1x < 0:
            pt1x = 0
            pt1y = pt2y
        if pt1x > fx:
            pt1x = fx
            pt1y = pt2y
        if pt2x < 0:
            pt2x = 0
            pt2y = pt1y
        if pt2x > fx:
            pt2x = fx
            pt2y = pt1y
        if pt2y > fy:
            pt2y = fy
            pt2x = pt1x
        if pt2y < 0:
            pt2y = 0
            pt2x = pt1x
        if pt1y < 0:
            pt1y = 0
            pt1x = pt2x
        if pt1y > fy:
            pt1y = fy
            pt1x = pt2x

    else:

        slope = float(pt2y - pt1y) / float(pt2x - pt1x)

        if pt1x < 0:
            pt1x = 0
            pt1y = pt2y - (slope * float(pt2x - pt1x))
        if pt1x > fx:
            pt1x = fx
            pt1y = pt2y - (slope * float(pt2x - pt1x))
        if pt2x < 0:
            pt2x = 0
            pt2y = pt1y + (slope * float(pt2x - pt1x))
        if pt2x > fx:
            pt2x = fx
            pt2y = pt1y + (slope * float(pt2x - pt1x))
        if pt2y > fy:
            pt2y = fy
            pt2x = pt1x + (float(pt2y - pt1y) / slope)
        if pt2y < 0:
            pt2y = 0
            pt2x = pt1x + (float(pt2y - pt1y) / slope)
        if pt1y < 0:
            pt1y = 0
            pt1x = pt2x - (float(pt2y - pt1y) / slope)
        if pt1y > fy:
            pt1y = fy
            pt1x = pt2x - (float(pt2y - pt1y) / slope)
    pt1 = (pt1x, pt1y)
    pt2 = (pt2x, pt2y)
    arrange_points(pt1, pt2)
    return (pt1, pt2)

def dist(p1, p2):
    p1x, p1y = p1
    p2x, p2y = p2
    return np.sqrt(np.square(p1x - p2x) + np.square(p1y - p2y))

def line_intersection(line1, line2):
    rho1, theta1 = line1
    rho2, theta2 = line2
    a1 = np.cos(theta1)
    a2 = np.cos(theta2)
    b1 = np.sin(theta1)
    b2 = np.sin(theta2)
    x = (rho1 * b2 - rho2 * b1) / (b2 * a1 - b1 * a2)
    y = (rho2 * a1 - rho1 * a2) / (b2 * a1 - a2 * b1)

    return x, y

def nearestNode(points):
    x_nearest = fx
    y_nearest = fy
    min_distance = 2 * fx + fy
    for (x, y) in points:
        present_dist = dist((x, y), (fx / 2, fy / 2))
        if min_distance > present_dist:
            x_nearest, y_nearest = (x, y)
            min_distance = present_dist
    return (x_nearest, y_nearest)


def takeoff((kpx, kix, kdx, kpy, kiy, kdy)):
    global vehicle    
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
    while_condition = True
    while while_condition:
        try:
            if _land==False:       
                setz = 1.0 
                currentz = vehicle.location.global_relative_frame.alt
                errorz = setz - currentz
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
                    while_condition = False
                print " Altitude: ", currentz , "errorz:", errorz,"setz",setz
                print "throttle",vehicle.channels['3'] 
            else:
                print "Keyboard Interrupt! Setting throttle 0"
                vehicle.channels.overrides['3']=0
                exit()
             
        except KeyboardInterrupt:
            vehicle.channels.overrides['3']=0    

def arm_and_takeoff(aTargetAltitude, (kpx, kix, kdx, kpy, kiy, kdy)):
    global _land
    global vehicle  
    
    # Arms vehicle and fly to aTargetAltitude.
    

    #print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    # while not vehicle.is_armable:
    #     print " Waiting for vehicle to initialise..."
    #     time.sleep(1)

        
    '''print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("ALT_HOLD")
    vehicle.armed=True 
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)   
    print "Taking off!"'''

    # Strating Camera
    print "Starting Camera"
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Output')

    while True:
        try:
            global fx
            global fy
            group_lines = []
            ret, pic = cap.read()
            try:
                fy, fx, channels = pic.shape
            except:
                continue
            img = cv2.cvtColor(pic, cv2.COLOR_BGR2YCR_CB)
            pic_bin = cv2.inRange(img, (99, 132, 81), (162, 164, 109))
            pic_bin = cv2.Canny(pic_bin, 50, 200, 3)
            rslt = cv2.cvtColor(pic_bin, cv2.COLOR_GRAY2BGR)
            lines = cv2.HoughLines(pic_bin, 1, np.pi / 180, 100)
            if np.size(lines) <= 1:
                continue

            # Group Lines
            for rho, theta in lines[0]:
                pt1, pt2 = line_points((rho, theta))
                rho1, theta1 = (rho, theta)
                meanRho = rho1
                meanTheta = theta1
                counter = 1
                flag_write = 0
                for j in range(0, len(group_lines)):
                    pt3, pt4 = line_points(group_lines[j])
                    rho2, theta2 = group_lines[j]
                    if (np.linalg.norm(dist(pt1, pt3)) + np.linalg.norm(dist(pt2, pt4))) < group_distance:
                        flag_write = 1
                        meanRho += rho2
                        meanTheta += theta2
                        counter += 1
                if flag_write == 0:
                    group_lines.append((meanRho / counter, meanTheta / counter))

            # Display grouped Lines
            for j in range(0, len(group_lines)):
                rho, theta = group_lines[j]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 2000 * (-b))
                y1 = int(y0 + 2000 * (a))
                x2 = int(x0 - 2000 * (-b))
                y2 = int(y0 - 2000 * (a))
                cv2.line(rslt, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # Find line intersections
            intersection_Points = []
            for i in range(0, len(group_lines)):
                for j in range(i, len(group_lines)):
                    x, y = line_intersection(group_lines[i], group_lines[j])
                    if x <= fx and y <= fy:
                        try:
                            intersection_Points.append((int(x), int(y)))
                            cv2.circle(rslt, (int(x), int(y)), 10, (255, 255, 255), thickness=1, lineType=8, shift=0)
                        except:
                            pass

            # Find nearest intersection
            x_nearest, y_nearest = nearestNode(intersection_Points)

            # Calculate PID error
            errorx = x_nearest - (fx / 2)
            errory = (fy / 2) - y_nearest
            cv2.circle(rslt, (x_nearest, y_nearest), 10, (0, 255, 255), thickness=1, lineType=8, shift=0)
            cv2.imshow('Output', rslt)

            print "dx: " + str(errorx)  + " dy: " + str(errory)
            # PID controller
            if _land==False:       
                setz = aTargetAltitude   
                currentz = vehicle.location.global_relative_frame.alt
                PIDx = 0
                PIDy = 0
                errorz = setz - currentz
                sum_errorx = 0
                prev_errorx = 0
                sum_errory = 0
                prev_errory = 0
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
                vehicle.channels.overrides['1'] = int(PIDx + 1500)  
                sum_errorx + sum_errorx + errorx
                prev_errorx = errorx
                print "errorx",errorx,"xthrottle",vehicle.channels['1']   
                PIDy = kpy*errory + kiy*sum_errory + kdy*prev_errory
                vehicle.channels.overrides['2'] = int(PIDy + 1500)  
                sum_errory + sum_errory + errory
                prev_errory = errory
                print "errory",errory,"ythrottle",vehicle.channels['2']
            else:
                print "Keyboard Interrupt! Setting throttle 0"
                vehicle.channels.overrides['3']=0
                exit()
             
        except KeyboardInterrupt:
            vehicle.channels.overrides['3']=0
           # vehicle.mode = VehicleMode("LAND")            
           # if _land:
            #    vehicle.channels.overrides['3']=1000
            #    exit()
            _land = True
        cv2.waitKey(33)


def main():
    global vehicle
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

    _pid_values = (kpx, kix, kdx, kpy, kiy, kdy)

    print _land
    takeoff(_pid_values)
    arm_and_takeoff(1, _pid_values)
        

main()
