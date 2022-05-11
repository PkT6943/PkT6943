import numpy as np
from operator import mul
import math


def pixelToWorld(coordinate):
    conversion_factor = 0.92
    world_XY_coordinate = coordinate * conversion_factor
    return world_XY_coordinate


def worldToPixel(co_ordinates):
    conversion_factor = 0.925
    pixel_XY_coordinate = [x / conversion_factor for x in co_ordinates]
    return pixel_XY_coordinate


def translate(point, x, y, z):
    x1 = point[0] + x
    y1 = point[1] + y
    return (x1, y1, z)


def rotate(point, theta):

    x = point[0]
    y = point[1]
    z = point[2]

    cosT = round(np.cos(np.radians(theta)), 3)
    sinT = round(np.sin(np.radians(theta)), 3)

    x1 = round(x*cosT - y*sinT, 2)
    y1 = round(x*sinT + y*cosT, 2)

    return [x1, y1, z]


def shiftCoordinateOriginToRobot(referencePoint_world):
    return (referencePoint_world[0]+84.3, referencePoint_world[1])


def convertRotationAngle360(rotationAngle):
    angle = round(rotationAngle)
    if angle < 0:
        angle = 360 + angle
    return angle
