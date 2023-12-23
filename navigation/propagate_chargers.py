import argparse
import os
import sys
import carla

from charger_stuff import create_charger
from draw_chargers import draw_chargers

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from interface.loading import get_chargers


def propagate(the_map:carla.Map, chargers:list, distance:float) -> list:
    """
    Propagates the given chargers backwards in their lanes.

    `map`: Map of the CARLA world
    `chargers`: List of chargers to propagate
    `distance`: Distance backwards to propagate chargers, in meters

    Returns a list of the new chargers created.
    """
    new_chargers = list()
    for charger in chargers:
        wp = the_map.get_waypoint(charger.center)
        new_wps = wp.previous(distance)
        if new_wps:
            new_chargers.append(
                create_charger(charger.length, charger.width, new_wps[0].transform, charger.max_power, charger.efficiency)
            )
    return new_chargers


def save_chargers(path, chargers):
    """
    Saves chargers to the file specified.

    `path`: Path to save file to.
    `chargers`: List of chargers to save.
    """
    with open(path, 'w') as file:
        file.write(f'front_left,front_right,back_right,power,efficiency\n')
        for charger in chargers:
            file.write(f'"({charger.front_left.x},{charger.front_left.y},{charger.front_left.z})"')
            file.write(f',"({charger.front_right.x},{charger.front_right.y},{charger.front_right.z})"')
            file.write(f',"({charger.back_right.x},{charger.back_right.y},{charger.back_right.z})"')
            file.write(f',{charger.max_power},{charger.efficiency}\n')


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'init_chargers',
        type=get_chargers,
        help='file to read initial chargers from'
    )
    argparser.add_argument(
        'outfile',
        help='file to save chargers to'
    )
    argparser.add_argument(
        'd',
        type=float,
        help='distance backwards to propagate'
    )
    argparser.add_argument(
        '--separate',
        action='store_true',
        help='only save new chargers in outfile'
    )
    argparser.add_argument(
        '-n',
        type=int,
        default=1,
        help='number of propagations to perform'
    )
    argparser.add_argument(
        '-i', '--interval',
        metavar='I',
        default=5.0,
        type=float,
        help='wait time for charger demonstration, or 0 to keep demonstration active'
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
    
    all_chargers = list() if args.separate else args.init_chargers
    new_chargers = args.init_chargers
    for _ in range(args.n):
        new_chargers = propagate(the_map, new_chargers, args.d)
        all_chargers += new_chargers

    save_chargers(args.outfile, all_chargers)
    draw_chargers(all_chargers, world.debug, args.interval)
