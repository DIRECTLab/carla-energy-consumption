import csv
import carla

from trackers.charger import Charger


def get_chargers(file):
    chargers = list()
    reader = csv.DictReader(file)
    for charger in reader:
        location = carla.Location(float(charger['x']), float(charger['y']), float(charger['z']))
        rotation = carla.Rotation(float(charger['pitch']), float(charger['yaw']), float(charger['roll']))
        transform = carla.Transform(location, rotation)
        dimensions = carla.Vector3D(float(charger['width']), float(charger['length']), float(charger['height']))
        chargers.append(Charger(transform, dimensions / 2))
    return chargers
