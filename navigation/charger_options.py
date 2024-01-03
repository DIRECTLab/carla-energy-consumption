#!/usr/bin/env python

import sys
import os
import argparse
import carla
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from navigation.charger_stuff import create_charger, display_options
from interface.loading import parse_location


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
        type=float,
        help='wait time between charger demonstrations, or 0 to keep demonstrations active; default no demonstrations'
    )
    argparser.add_argument(
        '-n', '--number',
        metavar='N',
        type=int,
        help='maximum number of options to display'
    )
    argparser.add_argument(
        '--power',
        type=float,
        help='add power field to output'
    )
    argparser.add_argument(
        '--efficiency',
        type=float,
        help='add efficiency field to output'
    )
    argparser.add_argument(
        '--seed',
        metavar='SEED',
        help='random seed'
    )
    argparser.add_argument(
        '-m', '--map',
        help='name of map to load, or "list" to list choices'
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
    random.seed(args.seed)

    client = carla.Client(args.host, args.port)
    client.set_timeout(20.0)

    if args.map is None:
        world = client.get_world()
    else:
        available_maps = [path.split('/')[-1] for path in client.get_available_maps()]
        if args.map == "list":
            print(available_maps)
            sys.exit()
        elif args.map in available_maps:
            world = client.load_world(args.map)
        else:
            print("Error: This map is not available.")
            sys.exit()

    if args.point is None:
        options = get_charger_options(world, args.length, args.width)
        random.shuffle(options)
    else:
        waypoint = world.get_map().get_waypoint(args.point)
        charger = create_charger(args.length, args.width, waypoint.transform)
        options = [charger]
    options = options[:args.number]

    display_options(world, options, args.interval, args.power, args.efficiency)
