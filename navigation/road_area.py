#!/usr/bin/env python

import argparse
import time
import carla


def lane_area(waypoints, separation) -> float:
    """
    Provides a reasonable estimate of the total area of the lane segments given.
    Assumes a constant waypoint separation.
    """
    area = 0.0
    for wp in waypoints:
        area += wp.lane_width * separation
    return area


def area_sums(bounding_boxes:list):
    area = 0.0
    for bounding_box in bounding_boxes:
        area += bounding_box.extent.x*bounding_box.extent.y*4
    return area


def junction_labels(world:carla.World, junction_bbs:list):
    search_area = area_sums(junction_bbs)
    area_searched = 0.0
    labeled_points = list()
    for junction_bb in junction_bbs:
        print(f'Searching junctions: {(area_searched/search_area)*100:.1f}%', end='\r')
        vertices = junction_bb.get_world_vertices(carla.Transform(rotation=junction_bb.rotation))
        min_x = min([vertex.x for vertex in vertices])
        max_x = max([vertex.x for vertex in vertices])
        min_y = min([vertex.y for vertex in vertices])
        max_y = max([vertex.y for vertex in vertices])
        min_z = min([vertex.z for vertex in vertices])
        max_z = max([vertex.z for vertex in vertices])
        z = max_z + 1
        search_depth = (z - min_z) + 1

        for x in range(round(min_x), round(max_x)+1, 1):
            for y in range(round(min_y), round(max_y)+1, 1):
                loc = carla.Location(x, y, z)
                proj = world.ground_projection(loc, search_depth)
                labeled_points.append(proj)
                # if proj is None:
                #     debug.draw_point(loc, life_time=15)
        area_searched += area_sums([junction_bb])
    print(f'Searching junctions: {(area_searched/search_area)*100:.1f}%')
    return labeled_points


def junction_label_counts(junction_labels):
    label_count = {
        label: 0
        for label in set([
            None if point is None else point.label 
            for point in junction_labels
        ])
    }
    for point in junction_labels:
        label = None if point is None else point.label
        label_count[label] += 1
    return label_count


def main(args):
    client = carla.Client(args.host, args.port)
    client.set_timeout(20.0)
    world = client.get_world()

    waypoints = world.get_map().generate_waypoints(args.lane_granularity)
    invalid_lanetypes = (
        carla.LaneType.Sidewalk,
        carla.LaneType.Tram,
        carla.LaneType.Rail,
    )
    vehicle_waypoints_junctions = list()
    vehicle_waypoints_no_junctions = list()
    for wp in waypoints:
        if wp.lane_type not in invalid_lanetypes:
            if wp.is_junction:
                vehicle_waypoints_junctions.append(wp)
            else:
                vehicle_waypoints_no_junctions.append(wp)

    lane_area_no_junctions = lane_area(vehicle_waypoints_no_junctions, args.lane_granularity)

    junctions = [wp.get_junction() for wp in vehicle_waypoints_junctions]
    junctions = {
        junction.id: junction.bounding_box
        for junction in junctions
    }

    settings = world.get_settings()
    was_rendering = not settings.no_rendering_mode
    if was_rendering:
        settings.no_rendering_mode = True
        world.apply_settings(settings)
    start = time.time()
    labels = junction_labels(world, list(junctions.values()))
    label_counts = junction_label_counts(labels)
    end = time.time()
    if was_rendering:
        settings.no_rendering_mode = False
        world.apply_settings(settings)

    print(f'Time: {end-start} s')
    print(f'{len(labels)} junction points searched')
    print(label_counts)

    unknown_area = label_counts.get(carla.CityObjectLabel.NONE, 0) + label_counts.get(None, 0)
    min_road_area = lane_area_no_junctions + label_counts.get(carla.CityObjectLabel.Roads, 0) + label_counts.get(carla.CityObjectLabel.RoadLines, 0)
    print(f'Total driveable road area is between {min_road_area:.0f} and {min_road_area+unknown_area:.0f} m^2.')
    print(f'Best guess: {min_road_area+label_counts.get(None, 0):.0f} m^2')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--lane-granularity',
        default=0.01,
        type=float,
        help='distance between points sampled on lanes outside of junctions'
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
    main(args)
