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
    if point is None: return
    return point.location.z


def show_coordinates(world:carla.World, time=0.1):
    """
    Highlights x- and y-axes at (0,0).
    """
    debug = world.debug
    height = get_elevation(carla.Location(), world) + 20
    length = 20
    x_end = carla.Location(length,0,height)
    debug.draw_arrow(carla.Location(0,0,height), x_end, thickness=1, arrow_size=2.5, color=carla.Color(255,200,0), life_time=time)
    debug.draw_string(x_end + carla.Vector3D(0,2,0), 'x', life_time=time)
    y_end = carla.Location(0,length,height)
    debug.draw_arrow(carla.Location(0,0,height), y_end, thickness=1, arrow_size=2.5, color=carla.Color(255,200,0), life_time=time)
    debug.draw_string(y_end + carla.Vector3D(0,2,0), 'y', life_time=time)


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
