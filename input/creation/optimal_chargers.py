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

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from input.creation.charger_stuff import create_charger, display_options


def get_vehicle_data(infolders) -> dict:
    """
    Returns all vehicle data as a dict of pandas DataFrames.
    `infolders`: List of paths to output from `multitracking.py`.
    """
    vehicle_data = dict()
    for infolder in infolders:
        vehicle_meta = pd.read_csv(os.path.join(infolder, "vehicles.csv"), index_col=0)
        for idx in vehicle_meta.index:
            data = pd.read_csv(os.path.join(infolder, f"vehicle{idx}.csv"), index_col=0)
            vehicle_data[f"{infolder}-{idx}"] = data
    return vehicle_data


def get_heatmap(xs, ys, unit_dim: float):
    """
    `xs`: list of x-coordinates
    `ys`: corresponding list of y-coordinates
    `unit_dim`: dimension of squares analyzed for visitation frequency

    Returns a tuple with the following values:
    - Histogram, represented as an np array
    - Dimension of each unit in the x direction. This should be similar to but slightly smaller than `unit_dim`
    - Dimension of each unit in the y direction. This should be similar to but slightly smaller than `unit_dim`
    """
    xrange = xs.ptp()
    xbins = math.ceil(xrange / unit_dim)
    xunit = xrange / xbins
    yrange = ys.ptp()
    ybins = math.ceil(yrange / unit_dim)
    yunit = yrange / ybins
    density, xedges, yedges = np.histogram2d(xs, ys, [xbins, ybins], density=True)
    return density, xunit, yunit


def get_chargers(xs, ys, unit_dim: float, n_chargers: int, length: float, width: float, the_map: carla.Map):
    """
    """
    density, xunit, yunit = get_heatmap(xs, ys, unit_dim)
    chargers = list()
    length_in_idxs = math.ceil(length / unit_dim)
    for _ in range(n_chargers):
        pop_idx = np.unravel_index(density.argmax(), density.shape)
        if density[pop_idx] == 0.0:
            break
        x = xs.min() + (pop_idx[0] + 0.5) * xunit
        y = ys.min() + (pop_idx[1] + 0.5) * yunit
        wp = the_map.get_waypoint(carla.Location(x, y, 0.0))
        charger = create_charger(length, width, wp.transform)
        chargers.append(charger)

        # This will exclude a square of size lengthxlength (plus a little extra). Is there a better option?
        for x_idx in range(pop_idx[0]-length_in_idxs, pop_idx[0]+length_in_idxs+1):
            if x_idx < density.shape[0]:
                for y_idx in range(pop_idx[1]-length_in_idxs, pop_idx[1]+length_in_idxs+1):
                    if y_idx < density.shape[1]:
                        density[x_idx, y_idx] = 0.0
    return chargers


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
        'n',
        metavar='N',
        type=int,
        help='maximum number of chargers to display'
    )
    argparser.add_argument(
        'infolders',
        nargs='+',
        metavar='INFOLDER',
        help='path to directory with simulation output data'
    )
    argparser.add_argument(
        '-i', '--interval',
        metavar='I',
        type=float,
        help='wait time between charger demonstrations, or 0 to keep demonstrations active; default no demonstrations'
    )
    argparser.add_argument(
        '-u', '--unit-dim',
        metavar='U',
        default=1.0,
        type=float,
        help='dimension of squares analyzed for visitation frequency'
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
    the_map = world.get_map()

    vehicle_data = get_vehicle_data(args.infolders)
    xs = np.concatenate([vehicle_data[idx]['x'].values for idx in vehicle_data.keys()])
    ys = np.concatenate([vehicle_data[idx]['y'].values for idx in vehicle_data.keys()])
    density, xunit, yunit = get_heatmap(xs, ys, args.unit_dim)
    chargers = get_chargers(xs, ys, args.unit_dim, args.n, args.length, args.width, the_map)
    display_options(world, chargers, args.interval, args.power, args.efficiency)
