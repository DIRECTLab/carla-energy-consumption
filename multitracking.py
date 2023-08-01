#!/usr/bin/env python

import argparse
import random
import carla

from loading import get_agents, get_chargers
from supervehicle import SuperVehicle
from reporting import save_all

class Simulation:
    def __init__(self, args) -> None:
        """
        Runs the simulation and saves the data collected.

        `args`: See `main()` below.
        """
        self.__args = args
        self.__actor_list = list()
        self.__ticking = False
        self.__world = None
        self.__spawn_points = None
        self.__available_spawn_points = None

        client = carla.Client(args.host, args.port)
        client.set_timeout(20.0)

        if self.__args.map is None:
            self.__world = client.get_world()
        else:
            available_maps = [path.split('/')[-1] for path in client.get_available_maps()]
            if self.__args.map == "list":
                print(available_maps)
                return
            elif self.__args.map in available_maps:
                self.__world = client.load_world(self.__args.map)
            else:
                print("Error: This map is not available.")
                return

        # Set traffic manager to normal speed (140% instead of default 70%). 
        # This kicks the default speed up to about 25 mph.
        self.__traffic_manager = client.get_trafficmanager()
        self.__traffic_manager.global_percentage_speed_difference(-40)

        settings = self.__world.get_settings()
        try:
            if self.__args.delta is not None:
                settings.fixed_delta_seconds = self.__args.delta
                if not self.__args.delta == 0 and not self.__args.asynch and not settings.synchronous_mode:
                    settings.synchronous_mode = True
                    self.__ticking = True
            if self.__ticking:
                self.__traffic_manager.set_synchronous_mode(True)
            if self.__args.render:
                settings.no_rendering_mode = not settings.no_rendering_mode
            self.__world.apply_settings(settings)

            if self.__args.seed is not None:
                random.seed(self.__args.seed)
                self.__traffic_manager.set_random_device_seed(self.__args.seed)

            map = self.__world.get_map()
            self.__spawn_points = map.get_spawn_points()
            self.__reset_available_spawn_points()

            self.__simulate()

        finally:
            if self.__ticking:
                settings.synchronous_mode = False
                self.__world.apply_settings(settings)
                self.__traffic_manager.set_synchronous_mode(False)

            if len(self.__actor_list) > 0:
                print('destroying actors . . .')
                client.apply_batch([carla.command.DestroyActor(sv.vehicle) for sv in self.__actor_list])
                print('done.')

    def __reset_available_spawn_points(self):
        self.__available_spawn_points = list(self.__spawn_points)
        random.shuffle(self.__available_spawn_points)

    def __spawn_vehicle(self, blueprint:carla.ActorBlueprint):
        """
        Tries every spawn point given until one is successful.
        
        return: The vehicle spawned, or `None` if none of the spawn points could be used.

        Side effect: Spawn points are removed from the list when tried.
        """
        vehicle = None
        while vehicle is None:
            try:
                transform = self.__available_spawn_points.pop()
            except IndexError:
                return None
            vehicle = self.__world.try_spawn_actor(blueprint, transform)
        return vehicle

    def __wait(self, seconds:float):
        """
        Waits until `seconds` simulation seconds have passed.
        """
        begin = self.__world.get_snapshot().timestamp.elapsed_seconds
        elapsed = 0
        while elapsed < seconds:
            if self.__ticking:
                self.__world.tick()
                snapshot = self.__world.get_snapshot()
            else:
                snapshot = self.__world.wait_for_tick()
            elapsed = snapshot.timestamp.elapsed_seconds - begin

    def __spawn_agent_class(self, agent_class:dict) -> list:
        """
        Parses a single dict from the list returned by `get_agents`.
        """
        # TODO: Set lane offsets
        supervehicles = list()
        blueprint_library = self.__world.get_blueprint_library()
        bp = blueprint_library.find(agent_class['vehicle'])
        if 'color' in agent_class.keys() and agent_class['color'] != '':
            bp.set_attribute('color', agent_class['color'])

        for _ in range(agent_class['number']):
            vehicle = self.__spawn_vehicle(bp)
            if vehicle is None:
                print('All spawn points have been filled. Pausing vehicle spawns.')
                self.__wait(seconds=5)
                self.__reset_available_spawn_points()
                vehicle = self.__spawn_vehicle(bp)
                if vehicle is None:
                    # Give up
                    break
            sv = SuperVehicle(vehicle, agent_class['agent_type'], agent_class['ev_params'], agent_class['init_soc'], agent_class['hvac'])
            if agent_class['agent_type'] == 'traffic_manager':
                self.__traffic_manager.vehicle_lane_offset(vehicle, agent_class['lane_offset'])
            supervehicles.append(sv)

        return supervehicles

    def __respawn(self, supervehicle:SuperVehicle):
        """
        Respawns a vehicle.
        """
        vehicle = supervehicle.vehicle
        blueprint_library = self.__world.get_blueprint_library()
        bp = blueprint_library.find(vehicle.type_id)
        bp.set_attribute('color', vehicle.attributes['color'])
        vehicle = self.__spawn_vehicle(bp)
        if vehicle is not None:
            supervehicle.reset_vehicle(vehicle)
            print(f'Respawned {vehicle.type_id}')

    def __simulate(self):
        try:
            tracked = list()
            for agent_class in self.__args.tracked:
                aclass_parsed = self.__spawn_agent_class(agent_class)
                self.__actor_list += aclass_parsed
                tracked += aclass_parsed

            for agent_class in self.__args.untracked:
                aclass_parsed = self.__spawn_agent_class(agent_class)
                self.__actor_list += aclass_parsed

            print(f"Total number of vehicles: {len(self.__actor_list)}")

            for supervehicle in self.__actor_list:
                supervehicle.choose_route(self.__spawn_points)

            # The first couple seconds of simulation are less reliable as the vehicles are dropped onto the ground.
            self.__wait(2)

            for supervehicle in tracked:
                supervehicle.initialize_trackers(self.__args.wireless_chargers)

            print(f'Tracking for {self.__args.time} seconds. Press Ctrl-C to interrupt.')
            while tracked[-1].time_tracker.time <= self.__args.time:
                if self.__ticking:
                    self.__world.tick()
                else:
                    self.__world.wait_for_tick()

                for supervehicle in self.__actor_list:
                    if not supervehicle.vehicle.is_alive:
                        self.__reset_available_spawn_points()
                        self.__respawn(supervehicle)
                    supervehicle.run_step(self.__spawn_points)

        except KeyboardInterrupt:
            pass

        finally:
            for supervehicle in tracked:
                for tracker in supervehicle.trackers:
                    tracker.stop()

            if len(self.__actor_list) > 0:
                print('Saving data . . .')
                save_all(self.__actor_list, self.__args.outfolder)


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
        '-t', '--time',
        metavar='T',
        type=float,
        default=float('inf'),
        help='number of simulation seconds to track; defualts to infinity'
    )
    argparser.add_argument(
        '-d', '--delta',
        metavar='D',
        type=float,
        help='amount of simulated time (in seconds) per step, or 0 for "real time"; sets synch mode unless 0 or --asynch is set'
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

    Simulation(args)


if __name__ == '__main__':
    main()
