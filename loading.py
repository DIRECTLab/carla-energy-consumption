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
    agent_classes = list()
    with open(path, 'r') as file:
        reader = csv.DictReader(file)
        for agent_class in reader:
            agent_class['number'] = int(agent_class['number'])
            agent_classes.append(agent_class)
    return agent_classes