import argparse
import time
import os
import sys
import carla

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from input.creation.charger_stuff import create_charger
from navigation.draw_chargers import draw_chargers


granularity = 1.0


def get_junction_chargers(world:carla.World, length:float, width:float) -> dict:
    """
    Creates chargers near the entrance to junctions.

    `world`: CARLA world
    `length`: Length of charger to create, in meters
    `width`: Width of charger to create, in meters

    Returns a dictionary whose keys are junction IDs and values are lists of chargers near those junctions.
    """
    waypoints = world.get_map().generate_waypoints(granularity)

    junctions = set()
    for wp in waypoints:
        if wp.is_junction:
            junctions.add(wp.get_junction().id)

    junction_chargers = {
        junction: list()
        for junction in junctions
    }
    for wp in waypoints:
        if not wp.is_junction:
            next_wp = wp.next(granularity)
            if next_wp and next_wp[0].is_junction:
                junction_chargers[next_wp[0].get_junction().id].append(create_charger(length, width, wp.transform))
    return junction_chargers

# create/update method that saves everything to one big file as well.


def save_chargers(path, chargers, big_file, power=None, efficiency=None):
    """
    Saves chargers to the file specified.

    `path`: Path to save file to.
    `chargers`: List of chargers to save.
    `power`: Value of `power` attribute, if any.
    `efficiency`: Value of `efficiency` attribute, if any.
    """
    power_str = '' if power is None else f',{power}'
    efficiency_str = '' if efficiency is None else f',{efficiency}'
    with open(path, 'w') as file:
        file.write(f'front_left,front_right,back_right')
        file.write(f'{",power" if power is not None else ""}')
        file.write(f'{",efficiency" if efficiency is not None else ""}\n')
        for charger in chargers:
            file.write(f'"({charger.front_left.x},{charger.front_left.y},{charger.front_left.z})"')
            big_file.write(f'"({charger.front_left.x},{charger.front_left.y},{charger.front_left.z})"')
            file.write(f',"({charger.front_right.x},{charger.front_right.y},{charger.front_right.z})"')
            big_file.write(f',"({charger.front_right.x},{charger.front_right.y},{charger.front_right.z})"')
            file.write(f',"({charger.back_right.x},{charger.back_right.y},{charger.back_right.z})"')
            big_file.write(f',"({charger.back_right.x},{charger.back_right.y},{charger.back_right.z})"')
            file.write(f'{power_str}{efficiency_str}\n')
            big_file.write(f'{power_str}{efficiency_str}\n')


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
        'outfolder',
        help='directory to save data to'
    )
    argparser.add_argument(
        '-i', '--interval',
        metavar='I',
        default=5.0,
        type=float,
        help='wait time between charger demonstrations, or 0 to keep demonstrations active'
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

    junction_chargers = get_junction_chargers(world, args.length, args.width)

    os.makedirs(args.outfolder, exist_ok=True)

    # new stuff here
    with open('all_junctions.csv', 'w') as file1:
        file1.write(f'front_left,front_right,back_right')
        file1.write(f'{",power" if args.power is not None else ""}')
        file1.write(f'{",efficiency" if args.efficiency is not None else ""}\n')
        for junction, chargers in junction_chargers.items():
            print(junction)
            save_chargers(os.path.join(args.outfolder, f'junction{junction}.csv'), chargers,file1, args.power, args.efficiency)
            draw_chargers(chargers, world.debug, args.interval)
            time.sleep(args.interval)
