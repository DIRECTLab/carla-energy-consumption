#!/usr/bin/env python

import argparse
import time
import carla
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loading import get_chargers


def draw_chargers(chargers:list, debug:carla.DebugHelper, time:float):
    """
    Highlights the wireless chargers specified. 
    Navigate beneath the ground to view wireless chargers placed there, 
    or place them at ground level as recommended.
    """
    for charger in chargers:
        charger.draw(debug, time)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'wireless_chargers',
        metavar='CHARGEFILE',
        type=get_chargers,
        help='CSV file to read wireless charging data from'
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

    tick_id = world.on_tick(lambda snapshot: draw_chargers(args.wireless_chargers, world.debug, time=0.1))
    try:
        print('Waiting for Ctrl-C')
        time.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        world.remove_on_tick(tick_id)
