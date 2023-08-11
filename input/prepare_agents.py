import argparse
import pathlib
import sys
import random
import csv


def agent_fields(args) -> dict:
    fields = dict()
    for idx in range(0, len(args), 2):
        try:
            fields[args[idx]] = args[idx+1]
        except IndexError:
            print('Error: Each constant field must provide a name and a value.')
            sys.exit(1)
    return fields


def prepare_agents(number, vehicle, agent_type, randomized_fields=list(), **kwargs) -> dict:
    agents = list()
    for _ in range(number):
        agent = kwargs.copy()
        agent['vehicle'] = vehicle
        agent['agent_type'] = agent_type
        for field in randomized_fields:
            if field == 'init_soc':
                agent['init_soc'] = random.random()
        agents.append(agent)
    return agents


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
        metavar='VEHICLE',
        help='vehicle blueprint'
    )
    argparser.add_argument(
        'agent_type',
        metavar='AGENT_TYPE',
        help='agent type'
    )
    argparser.add_argument(
        '-c', '--constants',
        metavar='FIELD VALUE',
        nargs='*',
        default=list(),
        help='any other fields with constant values, e.g. init_soc 0.8'
    )
    argparser.add_argument(
        '-r', '--randomize',
        metavar='FIELD',
        nargs='*',
        default=list(),
        help='fields to randomize values for'
    )
    argparser.add_argument(
        '--seed',
        metavar='SEED',
        help='random seed'
    )
    argparser.add_argument(
        '-o', '--out',
        type=pathlib.Path,
        help='file to write agents to (default: stdout)'
    )
    args = argparser.parse_args()
    args.constants = agent_fields(args.constants)
    if args.seed is not None:
        random.seed(args.seed)

    agents = prepare_agents(args.number, args.vehicle, args.agent_type, args.randomize, **args.constants)
    
    outfile = sys.stdout if args.out is None else open(args.out, 'w', newline='')
    writer = csv.DictWriter(outfile, agents[0].keys())
    writer.writeheader()
    writer.writerows(agents)
    if outfile is not sys.stdout:
        outfile.close()
