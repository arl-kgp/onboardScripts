import cv2
import numpy as np

fx = fy = 0
group_distance = 500

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


def main():
    cap = cv2.VideoCapture("out1.AVI")
    cv2.namedWindow('Control')

    while True:
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

        x_nearest, y_nearest = nearestNode(intersection_Points)
        cv2.circle(rslt, (x_nearest, y_nearest), 10, (0, 255, 255), thickness=1, lineType=8, shift=0)
        cv2.imshow('Control', rslt)
        cv2.waitKey(33)

main()