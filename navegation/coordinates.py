#!/usr/bin/env python

import argparse
import time
import carla


def get_elevation(location:carla.Location, world:carla.World):
    """
    Returns the height of the surface at `location`.
    """
    max_height = 99_999    # Max height (meters)
    location.z = max_height
    point = world.ground_projection(location, max_height * 2)
    if point is None: return None
    return point.location.z


def show_coordinates(world:carla.World, time=0.1):
    """
    Highlights x- and y-axes at (0,0).
    Each square is 1m x 1m.
    """
    debug = world.debug
    height = get_elevation(carla.Location(), world) + 20
    length = 20
    thickness = 1
    space = 1
    begin = 0
    end = space - thickness
    for _ in range(begin, length, space * 2):
        debug.draw_line(carla.Location(begin,0,height), carla.Location(end,0,height), thickness, color=carla.Color(255,200,0), life_time=time)
        debug.draw_line(carla.Location(0,begin,height), carla.Location(0,end,height), thickness, color=carla.Color(255,200,0), life_time=time)
        begin += space * 2
        end += space * 2
    debug.draw_arrow(carla.Location(begin,0,height), carla.Location(end+0.01,0,height), thickness, arrow_size=2, color=carla.Color(255,200,0), life_time=time)
    debug.draw_string(carla.Location(end,2,height), 'x', life_time=time)
    debug.draw_arrow(carla.Location(0,begin,height), carla.Location(0,end+.01,height), thickness, arrow_size=2, color=carla.Color(255,200,0), life_time=time)
    debug.draw_string(carla.Location(2,end,height), 'y', life_time=time)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
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

    tick_id = world.on_tick(lambda snapshot: show_coordinates(world))
    try:
        print('Waiting for Ctrl-C')
        time.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        world.remove_on_tick(tick_id)
