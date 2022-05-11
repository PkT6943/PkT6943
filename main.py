from email.mime import base
import cv2 as cv
import numpy as np
from jproperties import Properties

import modbus
import time
import helper
from orientation import processFrame
from coordinates import getAllCoordinates

# Main function


def main():

    configs = Properties()
    with open('main.properties', 'rb') as config_file:
        configs.load(config_file)

    CAMERA_WIDTH = float(configs.get("CAM_WIDTH").data)
    CAMERA_HEIGHT = float(configs.get("CAM_HEIGHT").data)
    CAMERA_FPS = float(configs.get("CAM_FPS").data)

    capture = cv.VideoCapture(1, cv.CAP_DSHOW)
    # set new dimensionns to cam object (not cap)
    capture.set(cv.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    capture.set(cv.CAP_PROP_FPS, CAMERA_FPS)

    FRAME_X_MIN = int(configs.get("FRAME_X_MIN").data)
    FRAME_X_MAX = int(configs.get("FRAME_X_MAX").data)
    FRAME_Y_MIN = int(configs.get("FRAME_Y_MIN").data)
    FRAME_Y_MAX = int(configs.get("FRAME_Y_MAX").data)

    time.sleep(3)

    ret, frame = capture.read()
    ret, frame = capture.read()
    crop_frame = frame[FRAME_Y_MIN:FRAME_Y_MAX, FRAME_X_MIN:FRAME_X_MAX]

    # Process the frame to get the reference point (M5 button center) pixel coordinates and the rotation angle of the box
    (center, rotationAngle) = processFrame(crop_frame, configs)
    cv.imshow("Frames", frame)

    # Convert the pixel coordinates of M5 reference point to world coordinates in mm
    referencePoint_world = (helper.pixelToWorld(
        center[0]), helper.pixelToWorld(center[1]))

    # Shift the origin of the reference point from camera origin to robot origin
    robot_coordinates_reference = helper.shiftCoordinateOriginToRobot(
        referencePoint_world)

    # Convert rotation angle scale from 180,-180 to 360
    rotationAngle = helper.convertRotationAngle360(rotationAngle)

    # Get coordinates for all elements
    objects = getAllCoordinates(robot_coordinates_reference, rotationAngle)

    # Establish modbus connection with the robot and send coodinates
    client = modbus.configure("194.94.86.6", 502)

    # Send rotation angle at address 24576
    base_address = 24576
    modbus.sendAngleValue(client, base_address, rotationAngle)

    # Send each coordinate starting from address 24576
    base_address = base_address + 1
    for key, value in objects.items():
        print("Sending coordinates for ", key, " at address ", base_address)
        x = value[0]
        y = value[1]
        z = value[2]
        try:
            modbus.sendPointCoordinates(client, base_address, x, y, z)
            print("Sent coordinates - ", x, y, z)
        except:
            print("Modbus communication failure while sending coordinates for ", key)
            break
        base_address = base_address + 3

    k = cv.waitKey(0)
    if k == ord('q'):
        capture.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()
