#!/usr/bin/env python

# Copyright (c) 2019 Intel Labs
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Welcome to CARLA manual control with steering wheel Logitech G29.

To drive start by preshing the brake pedal.
Change your wheel_config.ini according to your steering wheel.

To find out the values of your steering wheel use jstest-gtk in Ubuntu.

"""

from __future__ import print_function

import carla

import argparse
import logging

import pygame

from interface.hud import HUD
from interface.world import World
from interface.loading import get_agents, get_chargers
from interface.reporting import save_vehicle_data
from interface.wheel.carla_control import CarlaControl


class Simulation:
    def __init__(self, args) -> None:
        """
        Runs the simulation and saves the data collected.

        `args`: See `main()` below.
        """
        pygame.init()
        pygame.font.init()
        self.__world = None

        try:
            client = carla.Client(args.host, args.port)
            client.set_timeout(60.0)

            self.__display = pygame.display.set_mode(
                (args.width, args.height),
                pygame.HWSURFACE | pygame.DOUBLEBUF)

            self.__hud = HUD(args.width, args.height, help=__doc__)
            self.__world = World(
                client.get_world(), 
                self.__hud, 
                args.tracked[0]['vehicle'], 
                args.tracked[0]['ev_params'], 
                args.wireless_chargers, 
                args.tracked[0]['init_soc'], 
                args.tracked[0]['hvac']
            )
            self.__controller = CarlaControl(self.__world, args.autopilot)

            self.__simulate(args.out)

        finally:
            if self.__world is not None:
                self.__world.destroy()
            pygame.quit()

    def __simulate(self, file=None):
        # The first couple seconds of simulation are less reliable as the vehicles are dropped onto the ground.
        self.__world.wait(2.0)
        try:
            self.__world.initialize_trackers()
            self.__world.wait(1.0)

            clock = pygame.time.Clock()
            while True:
                clock.tick_busy_loop(60)
                if self.__controller.parse_events(self.__world):
                    return
                self.__world.tick(clock)
                self.__world.render(self.__display)
                pygame.display.flip()
        finally:
            if file is not None:
                self.__world.destroy()
                print('Saving data . . .')
                save_vehicle_data(self.__world.trackers.values(), file)


# ==============================================================================
# -- main() --------------------------------------------------------------------
# ==============================================================================


def main():
    argparser = argparse.ArgumentParser(description='CARLA Manual Control Client')
    argparser.add_argument(
        'tracked',
        metavar='TRACKEDFILE',
        type=get_agents,
        help="CSV file for this agent's parameters"
    )
    argparser.add_argument(
        '-o', '--out',
        metavar='FILE',
        default=None,
        help='CSV file to write tracking data to'
    )
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='debug',
        help='print debug information')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-a', '--autopilot',
        action='store_true',
        help='enable autopilot')
    argparser.add_argument(
        '--res',
        metavar='WIDTHxHEIGHT',
        default='1280x720',
        help='window resolution (default: 1280x720; maintain the ratio)')
    argparser.add_argument(
        '-w', '--wireless-chargers',
        metavar='CHARGEFILE',
        type=get_chargers,
        default=list(),
        help='CSV file to read wireless charging data from'
    )
    args = argparser.parse_args()

    args.width, args.height = [int(x) for x in args.res.split('x')]

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    print(__doc__)

    try:

        Simulation(args)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':

    main()
