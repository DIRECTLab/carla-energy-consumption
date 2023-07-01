import argparse
import random
import carla

from agents.navigation.behavior_agent import BehaviorAgent
from agents.navigation.basic_agent import BasicAgent
from agents.navigation.constant_velocity_agent import ConstantVelocityAgent

from loading import get_agents, yes_no, get_chargers
from supervehicle import SuperVehicle
from reporting import save_data
from trackers.time_tracker import TimeTracker
from trackers.soc_tracker import SocTracker
from trackers.kinematics_tracker import KinematicsTracker
from trackers.ev import EV

"""
This module seeks to combine the best of `example.py` and `automatic_control.py`.
"""


def spawn_agent_class(agent_class:dict, world:carla.World, spawn_points:list) -> list:
    """
    Parses a single dict from the list returned by `get_agents`.
    """
    supervehicles = list()
    blueprint_library = world.get_blueprint_library()
    bp = blueprint_library.find('vehicle.tesla.model3')
    bp.set_attribute('color', '204,255,11') # Lime green to make it visible

    for _ in range(agent_class['number']):
        transform = random.choice(spawn_points)
        vehicle = world.spawn_actor(bp, transform)
        spawn_points.remove(transform)
        print(f'created {vehicle.type_id} at {transform.location}')

        # https://arxiv.org/pdf/1908.08920.pdf%5D pg17
        drag = 0.23
        frontal_area = 2.22
        ev = EV(vehicle, capacity=50.0, A_f=frontal_area, C_D=drag)

        if agent_class['agent_type'] == 'traffic_manager':
            vehicle.set_autopilot(True)
        elif agent_class['agent_type'] == 'cautious_behavior':
            agent = BehaviorAgent(vehicle, 'cautious')
        elif agent_class['agent_type'] == 'normal_behavior':
            agent = BehaviorAgent(vehicle, 'normal')
        elif agent_class['agent_type'] == 'aggressive_behavior':
            agent = BehaviorAgent(vehicle, 'aggressive')
        elif agent_class['agent_type'] == 'basic':
            agent = BasicAgent(world.player, target_speed=30)
        elif agent_class['agent_type'] == 'constant':
            agent = ConstantVelocityAgent(world.player, target_speed=30)

        supervehicles.append(SuperVehicle(ev))
    return supervehicles


def simulate(args):
    actor_list = []

    settings = None
    traffic_manager = None
    tracked = list()

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

        map = world.get_map()
        spawn_points = map.get_spawn_points()
        random.shuffle(spawn_points)

        for agent_class in args.tracked:
            aclass_parsed = spawn_agent_class(agent_class, world, spawn_points)
            actor_list += aclass_parsed
            tracked += aclass_parsed

        # for _ in range(args.number_of_vehicles-1):
        #     bp = random.choice(blueprint_library.filter('vehicle'))

        #     for _ in range(5):  # Try spawning 5 times
        #         try:
        #             transform = spawn_points.pop()
        #         except IndexError:
        #             print('All spawn points have been filled.')
        #             break
        #         npc = world.try_spawn_actor(bp, transform)
        #         if npc is not None:
        #             actor_list.append(npc)
        #             npc.set_autopilot(True)
        #             break
        print(f"Total number of vehicles: {len(actor_list)}")

        # The first couple seconds of simulation are less reliable as the vehicles are dropped onto the ground.
        time_tracker = TimeTracker(tracked[-1].ev.vehicle)
        time_tracker.start()
        while time_tracker.time < 2:
            if args.asynch:
                world.wait_for_tick()
            else:
                world.tick()
        time_tracker.stop()

        for vehicle in tracked:
            time_tracker = TimeTracker(vehicle.ev.vehicle)
            kinematics_tracker = KinematicsTracker(vehicle.ev.vehicle)
            soc_tracker = SocTracker(vehicle.ev, hvac=0.0, init_soc=0.80, wireless_chargers=args.wireless_chargers)
            vehicle.trackers = [time_tracker, kinematics_tracker, soc_tracker]
            for tracker in vehicle.trackers:
                tracker.start()

        while True:
            if args.asynch:
                world.wait_for_tick()
            else:
                world.tick()

    except KeyboardInterrupt:
        for vehicle in tracked:
            for tracker in vehicle.trackers:
                tracker.stop()

        # if args.output is not None:
        #     save_data(vehicle.trackers, args.output)

    finally:
        for vehicle in tracked:
            for tracker in vehicle.trackers:
                tracker.stop()

        if not args.asynch and settings is not None:
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
    # argparser.add_argument(
    #     '-u', '--untracked',
    #     metavar='UNTRACKEDFILE',
    #     type=get_agents,
    #     help='CSV file for untracked agent specifications'
    # )
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
        metavar='OUTPUTPATH',
        help='Directory to write tracking data to'
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
