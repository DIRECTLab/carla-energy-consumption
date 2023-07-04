#!/usr/bin/env python

# Adapted from tutorial.py (Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).)
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import random
import time
import csv
import argparse
import carla

from loading import yes_no, get_chargers
from reporting import print_update, save_data
from trackers.time_tracker import TimeTracker
from trackers.soc_tracker import SocTracker
from trackers.kinematics_tracker import KinematicsTracker
from trackers.ev import EV


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--number-of-vehicles',
        metavar='N',
        default=50,
        choices=range(1, 151),
        type=int,
        help='number of vehicles (default: 50)'
    )
    argparser.add_argument(
        '-m', '--map',
        help='name of map to load, or "list" to list choices'
    )
    argparser.add_argument(
        '-s', '--spawn-point',
        metavar=('X', 'Y', 'Z'),
        nargs=3,
        type=float,
        help='pick nearest spawn point to this coordinate for ego vehicle'
    )
    argparser.add_argument(
        '-t', '--time-step',
        metavar='T',
        type=float,
        help='amount of simulated time per step (seconds), or 0 for variable time step; set synch mode unless 0 or --asynch is set'
    )
    argparser.add_argument(
        '--asynch',
        action='store_true',
        help='run in asynch mode, considered less reliable'
    )
    argparser.add_argument(
        '-r', '--render',
        metavar='Y/N',
        type=yes_no,
        help='use rendering mode (y/n)'
    )
    argparser.add_argument(
        '-w', '--wireless-chargers',
        metavar='CHARGEFILE',
        type=get_chargers,
        default=list(),
        help='CSV file to read wireless charging data from'
    )
    argparser.add_argument(
        '-p', '--path',
        metavar='PATHFILE',
        type=argparse.FileType('r'),
        help='CSV file to read path instructions from'
    )
    argparser.add_argument(
        '-d', '--directions',
        metavar='DIRECTIONSFILE',
        type=argparse.FileType('r'),
        help='CSV file to read vehicle directions from'
    )
    argparser.add_argument(
        '-o', '--output',
        metavar='OUTPUTFILE',
        type=argparse.FileType('w'),
        help='Name of file to write tracking data to'
    )
    args = argparser.parse_args()

    actor_list = []

    settings = None
    traffic_manager = None
    camera = None
    trackers = None

    try:
        client = carla.Client('127.0.0.1', 2000)
        client.set_timeout(20.0)

        world = None
        if args.map is None:
            world = client.get_world()
        else:
            available_maps = [path.split('/')[-1] for path in client.get_available_maps()]
            if args.map == "list":
                print(available_maps)
                return
            elif args.map in available_maps:
                world = client.load_world(args.map)
            else:
                print("Error: This map is not available.")
                return

        # Set traffic manager to normal speed (140% instead of default 70%). 
        # This kicks the default speed up to about 25 mph.
        traffic_manager = client.get_trafficmanager()
        traffic_manager.global_percentage_speed_difference(-40)

        settings = world.get_settings()
        if args.time_step is not None:
            settings.fixed_delta_seconds = args.time_step
            if args.time_step == 0:
                args.asynch = True
            settings.synchronous_mode = not args.asynch
            world.apply_settings(settings)
            traffic_manager.set_synchronous_mode(not args.asynch)
        if args.render is not None:
            settings.no_rendering_mode = not args.render
            world.apply_settings(settings)

        blueprint_library = world.get_blueprint_library()

        bp = blueprint_library.find('vehicle.tesla.model3')

        bp.set_attribute('color', '204,255,11') # Lime green to make it visible

        bp.set_attribute('role_name', 'hero')
        traffic_manager.set_hybrid_physics_mode(True)
        traffic_manager.set_respawn_dormant_vehicles(True)

        map = world.get_map()
        spawn_points = map.get_spawn_points()
        if args.spawn_point is None:
            ego_transform = random.choice(spawn_points)
        else:
            choice_location = carla.Location(args.spawn_point[0], args.spawn_point[1], args.spawn_point[2])
            ego_transform = sorted(spawn_points, key=lambda point: point.location.distance(choice_location))[0]
        vehicle = world.spawn_actor(bp, ego_transform)
        spawn_points.remove(ego_transform)
        random.shuffle(spawn_points)

        actor_list.append(vehicle)
        print(f'created {vehicle.type_id} at {ego_transform.location}')

        path = list()
        if args.path is not None:
            reader = csv.DictReader(args.path)
            for loc in reader:
                location = carla.Location(float(loc['x']), float(loc['y']), float(loc['z']))
                path.append(location)
        traffic_manager.set_path(vehicle, path)

        route = list()
        if args.directions is not None:
            reader = csv.DictReader(args.directions)
            for loc in reader:
                route.append(loc['direction'])
        traffic_manager.set_route(vehicle, route)

        physics_vehicle = vehicle.get_physics_control()
        mass = physics_vehicle.mass
        print(f"Mass: {mass} kg")
        # https://arxiv.org/pdf/1908.08920.pdf%5D pg17
        drag = 0.23
        frontal_area = 2.22
        ev = EV(vehicle, capacity=50.0, A_f=frontal_area, C_D=drag)

        vehicle.set_autopilot(True)

        for _ in range(args.number_of_vehicles-1):
            bp = random.choice(blueprint_library.filter('vehicle'))

            for _ in range(5):  # Try spawning 5 times
                try:
                    transform = spawn_points.pop()
                except IndexError:
                    print('All spawn points have been filled.')
                    break
                npc = world.try_spawn_actor(bp, transform)
                if npc is not None:
                    actor_list.append(npc)
                    npc.set_autopilot(True)
                    break
        print(f"Total number of vehicles: {len(actor_list)}")

        # The first couple seconds of simulation are less reliable as the vehicles are dropped onto the ground.
        time_tracker = TimeTracker(vehicle)
        time_tracker.start()
        while time_tracker.time < 2:
            if args.asynch:
                world.wait_for_tick()
            else:
                world.tick()

        time_tracker = TimeTracker(vehicle)
        kinematics_tracker = KinematicsTracker(vehicle)
        soc_tracker = SocTracker(ev, hvac=0.0, init_soc=0.80, wireless_chargers=args.wireless_chargers)
        trackers = [time_tracker, kinematics_tracker, soc_tracker]
        for tracker in trackers:
            tracker.start()

        start = time.time()
        t = start
        display_clock = t
        # while t < start + 100:
        # while True:
        while time_tracker.time < 8028:
            if args.asynch:
                world.wait_for_tick()
            else:
                world.tick()
            t = time.time()

            if t - display_clock > 1:
                print_update(time_tracker, kinematics_tracker, soc_tracker)
                display_clock = t

        print(f'Finished in {t-start} seconds.')
        raise KeyboardInterrupt

    except KeyboardInterrupt:
        for tracker in trackers:
            tracker.stop()

        if args.output is not None:
            save_data(trackers, args.output)

    finally:
        if trackers is not None:
            for tracker in trackers:
                tracker.stop()

        if not args.asynch and settings is not None:
            settings.synchronous_mode = False
            world.apply_settings(settings)
            traffic_manager.set_synchronous_mode(False)

        if camera is not None:
            camera.destroy()
        if len(actor_list) > 0:
            print('destroying actors')
            client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
            print('done.')


if __name__ == '__main__':
    main()
