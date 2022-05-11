import cv2 as cv
import numpy as np
from jproperties import Properties
import helper


def getAllCoordinates(referencePoint, rotationAngle):

    translate_factors = {
        "initial_key_hole": [],
        "final_key_hole": [],
        "eth_point_1": [],
        "eth_point_2": [],
        "li_battery_opener": [],
        "red_button_above": [],
        "blue_button_above": [],
        "red_button_pressed": [],
        "blue_button_pressed": [],
        "battery_cover_remover": [],
        "battery_remove_point_01": [],
        "battery_remove_point_02": [],
        "battery_grip_point_01": [],
        "battery_grip_point_02": [],
        "battery_final_point_01": [],
        "battery_final_point_02": []
    }

    world_coordinates = {
        "initial_key_hole": [],
        "final_key_hole": [],
        "eth_point_1": [],
        "eth_point_2": [],
        "li_battery_opener": [],
        "red_button_above": [],
        "blue_button_above": [],
        "red_button_pressed": [],
        "blue_button_pressed": [],
        "battery_cover_remover": [],
        "battery_remove_point_01": [],
        "battery_remove_point_02": [],
        "battery_grip_point_01": [],
        "battery_grip_point_02": [],
        "battery_final_point_01": [],
        "battery_final_point_02": []
    }

    # Load properties file to get translation points of all elements from the reference element M5
    configs = Properties()
    with open('coordinates.properties', 'rb') as config_file:
        configs.load(config_file)

    # Fetch data from the properties file and store it in the translate_factors dictionary
    for keys, values in translate_factors.items():
        data_str = configs.get(keys).data
        data = data_str.split(",")
        values.append(float(data[0]))
        values.append(float(data[1]))
        values.append(float(data[2]))

    # Apply rotation to all points
    for key, value in translate_factors.items():
        rotated_point = helper.rotate(value, rotationAngle)
        translate_factors[key] = rotated_point

    print(translate_factors)

    # Find coordinated for all objects
    for key, value in translate_factors.items():
        point = referencePoint
        x = value[0]
        y = value[1]
        z = value[2]
        world_coordinates[key] = helper.translate(point, x, y, z)

    print(world_coordinates)
    return world_coordinates


getAllCoordinates((200, 100), 50)
