#!/usr/bin/env python

import sys
import os
import argparse
import carla
import random
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trackers.charger import Charger
from loading import parse_location


def get_charger_options(world:carla.World, length:float, width:float) -> list:
    """
    Returns a list of wireless charger placement options.
    """
    options = list()
    the_map = world.get_map()
    spawn_points = the_map.get_spawn_points()
    for spawn_point in spawn_points:
        rotation = spawn_point.rotation
        down_unit = carla.Location() - rotation.get_up_vector()
        center = world.project_point(spawn_point.location, down_unit, 5.0).location
        if center is None:
            center = spawn_point.location
        transform = carla.Transform(center, rotation)
        charger = create_charger(length, width, transform)
        options.append(charger)
    return options


def create_charger(length:float, width:float, center_transform:carla.Transform) -> Charger:
    forward_unit = center_transform.rotation.get_forward_vector()
    forward = forward_unit * length / 2
    right_unit = center_transform.rotation.get_right_vector()
    right = right_unit * width / 2

    front_left = center_transform.location + forward - right
    front_right = center_transform.location + forward + right
    back_right = center_transform.location + right - forward
    return Charger(front_left, front_right, back_right, power=0.0, efficiency=0.0)


def display_options(options:list, interval:float):
    print('front_left,front_right,back_right')
    for charger in options:
        charger.draw(world.debug, interval)
        print(f'"({charger.front_left.x},{charger.front_left.y},{charger.front_left.z})",', end='')
        print(f'"({charger.front_right.x},{charger.front_right.y},{charger.front_right.z})",', end='')
        print(f'"({charger.back_right.x},{charger.back_right.y},{charger.back_right.z})"')
        time.sleep(interval)


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
        '-p', '--point',
        metavar='(X,Y,Z)',
        type=parse_location,
        help='approximate charger center location'
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

    if args.point is None:
        options = get_charger_options(world, args.length, args.width)
        random.shuffle(options)
    else:
        waypoint = world.get_map().get_waypoint(args.point)
        charger = create_charger(args.length, args.width, waypoint.transform)
        options = [charger]

    display_options(options, args.interval)
