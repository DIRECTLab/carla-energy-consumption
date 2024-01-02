"""
Uses data from a previous simulation run to put chargers in the best places.
"""
import os
import sys
import math
import argparse
import numpy as np
import pandas as pd
import carla

from charger_stuff import create_charger


if __name__ == "__main__":
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
        'infolder',
        help='folder with simulation output data to use for determining optimal placement'
    )
    # argparser.add_argument(
    #     '-i', '--interval',
    #     metavar='I',
    #     default=5.0,
    #     type=float,
    #     help='wait time between charger demonstrations, or 0 to keep demonstrations active'
    # )
    argparser.add_argument(
        'n',
        type=int,
        help='maximum number of chargers to display'
    )
    argparser.add_argument(
        '-u', '--unit-dim',
        metavar='U',
        default=0.5,
        type=float,
        help='dimension of units to analyze for visitation frequency'
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
