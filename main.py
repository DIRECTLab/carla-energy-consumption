import argparse
import carla

from loading import get_agents, yes_no, get_chargers
from reporting import print_update, save_data

"""
This module seeks to combine the best of `example.py` and `automatic_control.py`.
"""


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
        '-s', '--spawn-point',
        metavar=('X', 'Y', 'Z'),
        nargs=3,
        type=float,
        help='pick nearest spawn point to this coordinate for ego vehicle'
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


if __name__ == '__main__':
    main()
