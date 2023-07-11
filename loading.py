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


def get_chargers(path) -> list:
    """
    Loads chargers from the CSV at `path`.
    """
    chargers = list()
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for charger in reader:
            location = carla.Location(float(charger['x']), float(charger['y']), float(charger['z']))
            rotation = carla.Rotation(float(charger['pitch']), float(charger['yaw']), float(charger['roll']))
            transform = carla.Transform(location, rotation)
            dimensions = carla.Vector3D(float(charger['width']), float(charger['length']), float(charger['height']))
            chargers.append(Charger(transform, dimensions / 2))
    return chargers


def get_agents(path) -> list:
    """
    Loads the agents from the CSV at `path`.
    """
    regular_params = ['vehicle', 'agent_type', 'number', 'color', 'hvac',]
    # EV params are used to create an EV object
    ev_params = ['capacity', 'A_f', 'gravity', 'C_r', 'c_1', 'c_2', 'rho_Air', 'C_D', 'motor_efficiency', 'driveline_efficiency', 'braking_alpha',]
    defaults = {
        'number': 1,
        'hvac': 0.0,
        'capacity': 50.0,
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
