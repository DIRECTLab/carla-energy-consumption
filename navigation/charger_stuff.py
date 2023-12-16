"""
Charger stuff shared between scripts in this directory.
"""


import os
import sys
import carla

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from interface.trackers.charger import Charger


def create_charger(length:float, width:float, center_transform:carla.Transform, power=0.0, efficiency=0.0) -> Charger:
    forward_unit = center_transform.rotation.get_forward_vector()
    forward = forward_unit * length / 2
    right_unit = center_transform.rotation.get_right_vector()
    right = right_unit * width / 2

    front_left = center_transform.location + forward - right
    front_right = center_transform.location + forward + right
    back_right = center_transform.location + right - forward
    return Charger(front_left, front_right, back_right, power, efficiency)
