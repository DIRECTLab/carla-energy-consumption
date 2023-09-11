#!/usr/bin/env python

import argparse
import carla


def main(args):
    client = carla.Client(args.host, args.port)
    client.set_timeout(20.0)
    world = client.get_world()

    waypoints = world.get_map().generate_waypoints(args.lane_granularity)
    invalid_lanetypes = (
        carla.LaneType.Sidewalk,
        carla.LaneType.Tram,
        carla.LaneType.Rail,
    )
    vehicle_waypoints_junctions = list()
    vehicle_waypoints_no_junctions = list()
    for wp in waypoints:
        if wp.lane_type not in invalid_lanetypes:
            if wp.is_junction:
                vehicle_waypoints_junctions.append(wp)
            else:
                vehicle_waypoints_no_junctions.append(wp)

    junctions_ld = len(vehicle_waypoints_junctions) * args.lane_granularity
    no_junctions_ld = len(vehicle_waypoints_no_junctions) * args.lane_granularity
    total_ld = junctions_ld + no_junctions_ld

    print(f'Lane distance in junctions:\t\t{junctions_ld:.2f} m')
    print(f'Lane distance outside junctions:\t{no_junctions_ld:.2f} m')
    print(f'Total lane distance:\t\t\t{total_ld:.2f} m')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--lane-granularity',
        default=0.01,
        type=float,
        help='distance between points sampled on lanes outside of junctions'
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
    main(args)
