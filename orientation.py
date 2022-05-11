import cv2 as cv
import numpy as np
import math

# M5 button and the Red button are the most significant objects on the box
# These boxes can be used for identifying box orientation
# Following function identifies these red buttons on the box in the frame


def findRotationAngle(frame, RED_BUTTON_AREA, M5_BUTTON_AREA):

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # define range of red color in HSV
    lower_red = np.array([0, 70, 50])
    upper_red = np.array([10, 255, 255])
    mask1 = cv.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 70, 50])
    upper_red = np.array([180, 255, 255])
    mask2 = cv.inRange(hsv, lower_red, upper_red)

    mask = mask1 | mask2

    contours, hierarchy = cv.findContours(
        mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    m5_button = (0, 0)
    red_button = (0, 0)
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > RED_BUTTON_AREA[0] and area < RED_BUTTON_AREA[1]:
            (x, y), radius = cv.minEnclosingCircle(cnt)
            red_button = (int(x), int(y))
            #radius = int(radius)
            # cv.circle(frame,red_button,radius,(0,255,255),2)
        elif area > M5_BUTTON_AREA[0] and area < M5_BUTTON_AREA[1]:
            (x, y), radius = cv.minEnclosingCircle(cnt)
            m5_button = (int(x), int(y))
            #radius = int(radius)
            # cv.circle(frame,m5_button,radius,(255,255,0),2)

    cv.line(frame, m5_button, red_button, (255, 0, 0), 1)

    deltaY = red_button[1] - m5_button[1]
    deltaX = red_button[0] - m5_button[0]

    angleInDegrees = math.atan2(deltaY, deltaX) * 180 / math.pi
    rotationAngle = int(math.trunc(-1 * ((angleInDegrees+24.1190344) - 90)))

    return (m5_button, rotationAngle)


# Function to process every frame
def processFrame(frame, configs):

    RED_BUTTON_AREA_MIN = int(configs.get("RED_BUTTON_MIN").data)
    RED_BUTTON_AREA_MAX = int(configs.get("RED_BUTTON_MAX").data)
    M5_BUTTON_AREA_MIN = int(configs.get("RED_BUTTON_M5_MIN").data)
    M5_BUTTON_AREA_MAX = int(configs.get("RED_BUTTON_M5_MAX").data)

    RED_BUTTON_AREA = (RED_BUTTON_AREA_MIN, RED_BUTTON_AREA_MAX)
    M5_BUTTON_AREA = (M5_BUTTON_AREA_MIN, M5_BUTTON_AREA_MAX)

    (center, rotationAngle) = findRotationAngle(
        frame, RED_BUTTON_AREA, M5_BUTTON_AREA)

    return (center, rotationAngle)
