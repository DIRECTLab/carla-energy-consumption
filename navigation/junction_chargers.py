import time
import carla

from charger_options import create_charger
from draw_chargers import draw_chargers


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

    for junction, chargers in junction_chargers.items():
        print(junction)
        # Save chargers
        draw_chargers(chargers, world.debug, interval)
        time.sleep(interval)
