import time
import os
import carla

from charger_options import create_charger
from draw_chargers import draw_chargers


def save_chargers(path, chargers, power=None, efficiency=None):
    """
    Saves chargers to the file specified.

    `path`: Path to save file to.
    `chargers`: List of chargers to save.
    `power`: Value of `power` attribute, if any.
    `efficiency`: Value of `efficiency` attribute, if any.
    """
    power_str = '' if power is None else f',{power}'
    efficiency_str = '' if efficiency is None else f',{efficiency}'
    with open(path, 'w') as file:
        file.write(f'front_left,front_right,back_right')
        file.write(f'{",power" if power is not None else ""}')
        file.write(f'{",efficiency" if efficiency is not None else ""}\n')
        for charger in chargers:
            file.write(f'"({charger.front_left.x},{charger.front_left.y},{charger.front_left.z})"')
            file.write(f',"({charger.front_right.x},{charger.front_right.y},{charger.front_right.z})"')
            file.write(f',"({charger.back_right.x},{charger.back_right.y},{charger.back_right.z})"')
            file.write(f'{power_str}{efficiency_str}\n')


if __name__ == "__main__":
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(20.0)
    world = client.get_world()

    granularity = 1.0
    length = 2.0
    width = 1.0
    out = 'chargertest/'
    interval = 5.0

    waypoints = world.get_map().generate_waypoints(granularity)

    junctions = set()
    for wp in waypoints:
        if wp.is_junction:
            junctions.add(wp.get_junction().id)

    junction_chargers = {
        junction: list()
        for junction in junctions
    }
    for wp in waypoints:
        if not wp.is_junction:
            next_wp = wp.next(granularity)
            if next_wp and next_wp[0].is_junction:
                junction_chargers[next_wp[0].get_junction().id].append(create_charger(length, width, wp.transform))

    os.makedirs(out, exist_ok=True)

    for junction, chargers in junction_chargers.items():
        print(junction)
        save_chargers(os.path.join(out, f'junction{junction}.csv'), chargers)
        draw_chargers(chargers, world.debug, interval)
        time.sleep(interval)
