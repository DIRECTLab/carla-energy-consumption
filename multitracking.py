import argparse
import random
import carla

from loading import get_agents, get_chargers
from supervehicle import SuperVehicle
from reporting import save_all

from trackers.time_tracker import TimeTracker
from trackers.soc_tracker import SocTracker
from trackers.kinematics_tracker import KinematicsTracker

"""
This module seeks to combine the best of `example.py` and `automatic_control.py`.
"""


def spawn_vehicle(blueprint:carla.ActorBlueprint, world:carla.World, spawn_points:list):
    """
    Tries every spawn point given until one is successful.
    
    return: The vehicle spawned, or `None` if none of the spawn points could be used.

    Side effect: Spawn points are removed from the list when tried.
    """
    vehicle = None
    while vehicle is None:
        try:
            transform = spawn_points.pop()
        except IndexError:
            print('All spawn points have been filled.')
            return None
        vehicle = world.try_spawn_actor(blueprint, transform)
    return vehicle


def spawn_agent_class(agent_class:dict, world:carla.World, spawn_points:list) -> list:
    """
    Parses a single dict from the list returned by `get_agents`.
    """
    supervehicles = list()
    blueprint_library = world.get_blueprint_library()
    bp = blueprint_library.find(agent_class['vehicle'])
    if 'color' in agent_class.keys():
        bp.set_attribute('color', agent_class['color'])

    for _ in range(agent_class['number']):
        vehicle = spawn_vehicle(bp, world, spawn_points)
        if vehicle is None:
            break
        sv = SuperVehicle(vehicle, agent_class['agent_type'], agent_class['ev_params'])
        supervehicles.append(sv)

    return supervehicles


def respawn(supervehicle:SuperVehicle, world:carla.World, spawn_points:list):
    """
    Respawns a vehicle.
    """
    vehicle = supervehicle.ev.vehicle
    blueprint_library = world.get_blueprint_library()
    bp = blueprint_library.find(vehicle.type_id)
    bp.set_attribute('color', vehicle.attributes['color'])
    vehicle = spawn_vehicle(bp, world, spawn_points)
    if vehicle is not None:
        supervehicle.reset_vehicle(vehicle)
        print(f'respawned {vehicle.type_id}')


def simulate(args):
    settings = None
    traffic_manager = None
    actor_list = list()
    tracked = list()
    ticking = False

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
            if not args.time_step == 0 and not args.asynch and not settings.synchronous_mode:
                settings.synchronous_mode = True
                ticking = True
        if ticking:
            traffic_manager.set_synchronous_mode(True)
        if args.render:
            settings.no_rendering_mode = not settings.no_rendering_mode
        world.apply_settings(settings)

        if args.seed is not None:
            random.seed(args.seed)
            traffic_manager.set_random_device_seed(args.seed)

        map = world.get_map()
        spawn_points = map.get_spawn_points()
        remaining_spawn_points = list(spawn_points)
        random.shuffle(remaining_spawn_points)

        for agent_class in args.tracked:
            aclass_parsed = spawn_agent_class(agent_class, world, remaining_spawn_points)
            actor_list += aclass_parsed
            tracked += aclass_parsed

        for agent_class in args.untracked:
            aclass_parsed = spawn_agent_class(agent_class, world, remaining_spawn_points)
            actor_list += aclass_parsed

        print(f"Total number of vehicles: {len(actor_list)}")

        for supervehicle in actor_list:
            supervehicle.choose_route(spawn_points)

        # The first couple seconds of simulation are less reliable as the vehicles are dropped onto the ground.
        time_tracker = TimeTracker(tracked[-1].ev.vehicle)
        time_tracker.start()
        while time_tracker.time < 2:
            if ticking:
                world.tick()
            else:
                world.wait_for_tick()
        time_tracker.stop()

        for supervehicle in tracked:
            time_tracker = TimeTracker(supervehicle.ev.vehicle)
            kinematics_tracker = KinematicsTracker(supervehicle.ev.vehicle)
            soc_tracker = SocTracker(supervehicle.ev, hvac=supervehicle.hvac, init_soc=0.80, wireless_chargers=args.wireless_chargers)
            supervehicle.trackers = [time_tracker, kinematics_tracker, soc_tracker]
            for tracker in supervehicle.trackers:
                tracker.start()

        while True:
            if ticking:
                world.tick()
            else:
                world.wait_for_tick()

            for supervehicle in actor_list:
                if not supervehicle.ev.vehicle.is_alive:
                    respawn_points = list(spawn_points)
                    random.shuffle(respawn_points)
                    respawn(supervehicle, world, respawn_points)
                supervehicle.run_step(spawn_points)

    except KeyboardInterrupt:
        pass

    finally:
        for supervehicle in tracked:
            for tracker in supervehicle.trackers:
                tracker.stop()

        if len(actor_list) > 0:
            print('saving data')
            save_all(actor_list, args.outfolder)

        if ticking:
            settings.synchronous_mode = False
            world.apply_settings(settings)
            traffic_manager.set_synchronous_mode(False)

        if len(actor_list) > 0:
            print('destroying actors')
            client.apply_batch([carla.command.DestroyActor(x.ev.vehicle) for x in actor_list])
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
        'outfolder',
        metavar='OUTFOLDER',
        help='directory to write tracking data to'
    )
    argparser.add_argument(
        '-u', '--untracked',
        metavar='UNTRACKEDFILE',
        type=get_agents,
        default=list(),
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
        action='store_true',
        help='toggle simulation rendering'
    )
    argparser.add_argument(
        '-w', '--wireless-chargers',
        metavar='CHARGEFILE',
        type=get_chargers,
        default=list(),
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
    argparser.add_argument(
        '--seed',
        metavar='SEED',
        type=int,
        help='random seed; guarantees determinism in synch mode'
    )
    args = argparser.parse_args()

    simulate(args)


if __name__ == '__main__':
    main()
