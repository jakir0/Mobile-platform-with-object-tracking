import cv2
import numpy as np
import imutils
from pololu_drv8835_rpi import motors, MAX_SPEED
import time
import math

#creating filtration kernel
kernel = np.ones((5,5),np.uint8)

#setting video capture source as default
cap = cv2.VideoCapture(0)

#limiting video feed resolution to speed up the program
cap.set(3,640)
cap.set(4,480)

#global variables
global hmin, hmax, smin, smax, vmin, vmax, min_radius, max_radius, m1, m2, k_m1, k_m2, l_turn, r_turn
m1 = 0 
m2 = 0
k_m1 = 1
k_m2 = 1
l_turn = 1
r_turn = 1

#START OF CALIBRATION(choosing tracked object)
def do_nothing(x):
    pass

#creating windows for program
cv2.namedWindow('Hue')
cv2.namedWindow('Saturation')
cv2.namedWindow('Value')
cv2.namedWindow('Closing')
cv2.namedWindow('Tracking')
#creating sliders for hue, saturation and value
cv2.createTrackbar('hmin', 'Hue',0,179,do_nothing)
cv2.createTrackbar('hmax', 'Hue',0,179,do_nothing)
cv2.createTrackbar('smin', 'Saturation',0,255,do_nothing)
cv2.createTrackbar('smax', 'Saturation',0,255,do_nothing)
cv2.createTrackbar('vmin', 'Value',0,255,do_nothing)
cv2.createTrackbar('vmax', 'Value',0,255,do_nothing)
while True:
    _,frame = cap.read()
    #conversion to HSV color space
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hue,sat,val = cv2.split(hsv)

    #getting values for tresholding
    hmin = cv2.getTrackbarPos('hmin','Hue')
    hmax = cv2.getTrackbarPos('hmax','Hue')
    smin = cv2.getTrackbarPos('smin','Saturation')
    smax = cv2.getTrackbarPos('smax','Saturation')
    vmin = cv2.getTrackbarPos('vmin','Value')
    vmax = cv2.getTrackbarPos('vmax','Value')

    #tresholding
    hthresh = cv2.inRange(np.array(hue),np.array(hmin),np.array(hmax))
    sthresh = cv2.inRange(np.array(sat),np.array(smin),np.array(smax))
    vthresh = cv2.inRange(np.array(val),np.array(vmin),np.array(vmax))

    #biwise AND for thresholded masks o n and j
    tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))

    #morpholigical filtering
    erosion = cv2.erode(tracking,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 2)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    closing = cv2.GaussianBlur(closing,(5,5),0)

    #finding contour and its center in mask
    #(x, y) geometric center of contour
    cnts = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    #executing if at least one contour if found
    if len(cnts) > 0:
        #finds the biggest countour in mask 
        #used for calculating minmial enclosing circle and its center
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        min_radius = round(radius - 15)
        max_radius = round(radius + 15)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        #program continues only if radius of circle is greater than given value
        if radius > 10:
        #drawing circle and its center
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    #showing results in windows
    cv2.imshow('Hue',hthresh)
    cv2.imshow('Saturation',sthresh)
    cv2.imshow('Value',vthresh)
    cv2.imshow('Closing',closing)
    cv2.imshow('Tracking',frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
time.sleep(5)
#END OF CALIBRATION

while True:
    _,frame = cap.read()

    #conversion to HSV color space
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hue,sat,val = cv2.split(hsv)

    # getting values for tresholding
    # tresholding
    hthresh = cv2.inRange(np.array(hue),np.array(hmin),np.array(hmax))
    sthresh = cv2.inRange(np.array(sat),np.array(smin),np.array(smax))
    vthresh = cv2.inRange(np.array(val),np.array(vmin),np.array(vmax))

    #biwise AND for thresholded masks o n and j
    tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))

    # morpholigical filtering
    erosion = cv2.erode(tracking,kernel,iterations = 2)
    dilation = cv2.dilate(erosion,kernel,iterations = 2)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    closing = cv2.GaussianBlur(closing,(5,5),0)

    #finding contour and its center in mask
    #(x, y) geometric center of contour
    cnts = cv2.findContours(closing.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    #executing if at least one contour if found
    if len(cnts) > 0:
        #finds the biggest countour in mask 
        #used for calculating minmial enclosing circle and its center
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        #program continues only if radius of circle is greater than given value
        if radius > 10:
            #drawing circle and its center
            cv2.circle(frame, (int(x), int(y)), int(radius),
            (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            #ENGINES CONTROL STARTS HERE
            #default values used for engines control


            #center of circle in correct position on x axis
            if x > 280 and x < 360 :
                l_turn = 1
                r_turn = 1

            #center of circle on the right side of platform 
            elif x > 360 :
                l_turn = (640 - x)/280
                r_turn = 1

            #center of circle on the left side of platform 
            elif x < 280 :
                r_turn = x/280
                l_turn = 1

            #platform if too far from tracked object
            #forward movment + turning
            if radius < min_radius :
                print('\nDriving forward')

                #engine 1
                stop_time = 0.01
                k_m1 = 1
                m1 = MAX_SPEED - (MAX_SPEED * math.fabs(radius/min_radius))
                m1 = l_turn * m1
                m1 = round(m1 * k_m1)

                #engine 2
                k_m2 = 1
                m2 = MAX_SPEED - (MAX_SPEED * math.fabs(radius/min_radius))
                m2 = r_turn * m2
                m2 = round(m2 * k_m2)
                
            #platform is at in correct distance from the tracked object

            elif radius > min_radius and radius < max_radius :
                #if tracked object is in the right position on x axis
                if x > 280 and x < 360:
                    print('\nSTOP')
                    m1 = 0
                    m2 = 0

                #center of circle is on the left side of platform 
                elif x > 360:
                    m1 =(MAX_SPEED/2)*(-1)
                    m1= m1 - m1 * l_turn
                    m2 = m1*(-1)
                    print("\nSTOP + turning left")

                #center of circle is on the right side of platform 
                elif x < 280:
                    m2 = (MAX_SPEED/2)*(-1)
                    m2 = m2 - m2 * r_turn
                    m1 = m2*(-1)
                    print("\nSTOP + turning right")

            #platform too close from the tracked object
            #driving backwars + turninig
            elif radius > max_radius:

                #engine 1
                print("\nDriving backwards")
                k_m1 = -1
                m1 = MAX_SPEED * math.fabs(radius/320)
                m1 = l_turn * m1
                m1 = round(m1 * k_m1)

                #engine 2
                k_m2 = -1
                m2 = MAX_SPEED * math.fabs(radius/320)
                m2 = r_turn * m2
                m2 = round(m2 * k_m2)

                #changing direction of turning while going backwards
                m1, m2 = m2, m1
            try:
                print("Engine 1 speed: ",int(m1))
                print("Engine 2 speed: ",int(m2))
                motors.setSpeeds(int(m1), int(m2))
                
            except:
                motors.setSpeeds(0, 0)

            finally:
                time.sleep(stop_time)
        else:
            motors.setSpeeds(0, 0)

    cv2.imshow('Tracking',frame)
    #exiting from loop if ESC key is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
motors.setSpeeds(0, 0)
