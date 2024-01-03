"""
Charger stuff shared between scripts in this directory.
"""


import os
import sys
import time
import carla

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from interface.trackers.charger import Charger


def create_charger(length:float, width:float, center_transform:carla.Transform, power=0.0, efficiency=0.0) -> Charger:
    forward_unit = center_transform.rotation.get_forward_vector()
    forward = forward_unit * length / 2.0
    right_unit = center_transform.rotation.get_right_vector()
    right = right_unit * width / 2.0

    front_left = center_transform.location + forward - right
    front_right = center_transform.location + forward + right
    back_right = center_transform.location + right - forward
    return Charger(front_left, front_right, back_right, power, efficiency)


def display_options(world:carla.World, options:list, interval:float=None, power:float=None, efficiency:float=None):
    print(f'front_left,front_right,back_right{",power" if power is not None else ""}{",efficiency" if efficiency is not None else ""}')
    power_str = ''
    if power is not None:
        power_str = f',{power}'
    efficiency_str = ''
    if efficiency is not None:
        efficiency_str = f',{efficiency}'
    for charger in options:
        print(f'"({charger.front_left.x},{charger.front_left.y},{charger.front_left.z})",', end='')
        print(f'"({charger.front_right.x},{charger.front_right.y},{charger.front_right.z})",', end='')
        print(f'"({charger.back_right.x},{charger.back_right.y},{charger.back_right.z})"{power_str}{efficiency_str}')
        if interval is not None:
            charger.draw(world.debug, interval)
            time.sleep(interval)
