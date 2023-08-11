import argparse
import sys
import csv


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'number',
        metavar='N',
        type=int,
        help='number of agents to prepare'
    )
    argparser.add_argument(
        'vehicle',
        help='vehicle blueprint'
    )
    argparser.add_argument(
        'agent_type',
        help='agent type'
    )
    argparser.add_argument(
        '--init_soc',
        help='add random init_soc parameter'
    )
    argparser.add_argument(
        'out',
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout
    )
    args = argparser.parse_args()

    agents = list()
    for _ in range(args.number):
        agent = {
            'vehicle': args.vehicle,
            'agent_type': args.agent_type,
        }
        agents.append(agent)


    writer = csv.DictWriter(args.out, ['vehicle', 'agent_type'])
    writer.writerows(agents)
