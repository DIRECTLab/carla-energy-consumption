#!/usr/bin/env python

import sys
import os
import argparse
import carla
import random
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trackers.charger import Charger


def get_charger_options(world:carla.World, length:float, width:float) -> list:
    """
    Returns a list of wireless charger placement options.
    """
    options = list()
    the_map = world.get_map()
    spawn_points = the_map.get_spawn_points()
    for spawn_point in spawn_points:
        center = spawn_point.location
        rotation = spawn_point.rotation
        forward_unit = rotation.get_forward_vector()
        forward = forward_unit * length / 2
        right_unit = rotation.get_right_vector()
        right = right_unit * width / 2
        front_left = center + forward - right
        front_right = center + forward + right
        back_right = center + right - forward
        charger = Charger(front_left, front_right, back_right, power=0.0, efficiency=0.0)
        options.append(charger)
    return options


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'length',
        metavar='L',
        type=float,
        help='length of the charger'
    )
    argparser.add_argument(
        'width',
        metavar='W',
        type=float,
        help='width of the charger'
    )
    argparser.add_argument(
        '-i', '--interval',
        metavar='I',
        default=5.0,
        type=float,
        help='wait time between charger demonstrations'
    )
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)'
    )
    argparser.add_argument(
        '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)'
    )
    args = argparser.parse_args()

    client = carla.Client(args.host, args.port)
    client.set_timeout(20.0)
    world = client.get_world()

    options = get_charger_options(world, args.length, args.width)
    random.shuffle(options)
    print('front_left,front_right,back_right')
    for charger in options:
        charger.draw(world.debug, args.interval)
        print(f'"{charger.front_left.x},{charger.front_left.y},{charger.front_left.z}",', end='')
        print(f'"{charger.front_right.x},{charger.front_right.y},{charger.front_right.z}",', end='')
        print(f'"{charger.back_right.x},{charger.back_right.y},{charger.back_right.z}"')
        time.sleep(args.interval)
