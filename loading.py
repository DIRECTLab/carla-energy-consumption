import csv
import carla

from trackers.charger import Charger


def yes_no(string: str):
    """
    Parses a y/n string.
    """
    string = string.lower()
    if string in ('y', 'yes', 'true'):
        return True
    if string in ('n', 'no', 'false'):
        return False
    return None


def parse_location(location_string:str) -> carla.Location:
    """
    Parses a string of the format
    `(X,Y,Z)`
    where `X`, `Y` and `Z` are numbers.
    """
    stripped = location_string[1:-1]
    listed = stripped.split(',')
    numbers = [float(n) for n in listed]
    return carla.Location(numbers[0], numbers[1], numbers[2])


def get_chargers(path) -> list:
    """
    Loads chargers from the CSV at `path`.
    """
    chargers = list()
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for charger in reader:
            front_left = parse_location(charger['front_left'])
            front_right = parse_location(charger['front_right'])
            back_right = parse_location(charger['back_right'])
            power = float(charger['power'])
            efficiency = float(charger['efficiency'])
            chargers.append(Charger(front_left, front_right, back_right, power, efficiency))
    return chargers


def get_agents(path) -> list:
    """
    Loads the agents from the CSV at `path`.
    """
    regular_params = ['vehicle', 'agent_type', 'number', 'color', 'hvac', 'init_soc', 'lane_offset',]
    # EV params are used to create an EV object
    ev_params = ['capacity', 'A_f', 'gravity', 'C_r', 'c_1', 'c_2', 'rho_Air', 'C_D', 'motor_efficiency', 'driveline_efficiency', 'braking_alpha',]
    defaults = {
        'number': 1,
        'hvac': 0.0,
        'capacity': 50.0,
        'init_soc': 0.80,
        'lane_offset': 0.0,
        'A_f': 2.3316,
        'gravity': 9.8066, 
        'C_r': 1.75, 
        'c_1': 0.0328, 
        'c_2': 4.575, 
        'rho_Air': 1.2256, 
        'C_D': 0.28,
        'motor_efficiency': 0.91, 
        'driveline_efficiency': 0.92, 
        'braking_alpha': 0.0411,
    }

    agent_classes = list()
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for agent_specification in reader:
            for option in defaults.keys():
                if option not in agent_specification.keys() or agent_specification[option] == '':
                    agent_specification[option] = defaults[option]
                else:
                    # Convert from str to correct type. Type must have a constructor that accepts str
                    agent_specification[option] = type(defaults[option])(agent_specification[option])

            agent_class = dict()
            for param in regular_params:
                if param in agent_specification.keys():
                    agent_class[param] = agent_specification[param]
            agent_class['ev_params'] = {param: agent_specification[param] for param in ev_params}
            agent_classes.append(agent_class)
    return agent_classes
