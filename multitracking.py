import argparse
import random
import time
import carla

from loading import get_agents, yes_no, get_chargers
from reporting import print_update, save_data
from trackers.time_tracker import TimeTracker
from trackers.soc_tracker import SocTracker
from trackers.kinematics_tracker import KinematicsTracker
from trackers.ev import EV

"""
This module seeks to combine the best of `example.py` and `automatic_control.py`.
"""


def simulate(args):
    actor_list = []

    settings = None
    traffic_manager = None
    trackers = None

    try:
        client = carla.Client(args.host, args.port)
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
        ego_transform = random.choice(spawn_points)
        vehicle = world.spawn_actor(bp, ego_transform)
        spawn_points.remove(ego_transform)
        random.shuffle(spawn_points)

        actor_list.append(vehicle)
        print(f'created {vehicle.type_id} at {ego_transform.location}')

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

        if len(actor_list) > 0:
            print('destroying actors')
            client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
            print('done.')


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'tracked',
        metavar='TRACKEDFILE',
        type=get_agents,
        help='CSV file for tracked agent specifications'
    )
    argparser.add_argument(
        '-u', '--untracked',
        metavar='UNTRACKEDFILE',
        type=get_agents,
        help='CSV file for untracked agent specifications'
    )
    argparser.add_argument(
        '-t', '--time-step',
        metavar='T',
        type=float,
        help='amount of simulated time per step (seconds), or 0 for variable time step; set synch mode unless 0 or --asynch is set'
    )
    argparser.add_argument(
        '-m', '--map',
        help='name of map to load, or "list" to list choices'
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
        '-o', '--output',
        metavar='OUTPUTFILE',
        type=argparse.FileType('w'),
        help='Name of file to write tracking data to'
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

    simulate(args)


if __name__ == '__main__':
    main()
