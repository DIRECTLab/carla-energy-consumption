import argparse
import time
import carla


def show_coordinates(debug:carla.DebugHelper, time=0.1):
    """
    Highlights x- and y-axes at the origin.
    """
    height = 20
    x_end = carla.Location(20,0,height)
    debug.draw_arrow(carla.Location(0,0,height), x_end, thickness=1, arrow_size=1, color=carla.Color(255,200,0), life_time=time)
    debug.draw_string(x_end + carla.Vector3D(0,2,0), 'x', life_time=time)
    y_end = carla.Location(0,20,height)
    debug.draw_arrow(carla.Location(0,0,height), y_end, thickness=1, arrow_size=1, color=carla.Color(255,200,0), life_time=time)
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

    tick_id = world.on_tick(lambda snapshot: show_coordinates(world.debug))
    try:
        print('Waiting for Ctrl-C')
        time.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        world.remove_on_tick(tick_id)
