#!/usr/bin/env python

# Adapted from tutorial.py (Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).)
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time
import csv
import math

import argparse
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

from time_tracker import TimeTracker
from soc_tracker import SocTracker
from kinematics_tracker import KinematicsTracker
from ev import EV
from charger import Charger


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '-n', '--number-of-vehicles',
        metavar='N',
        default=50,
        choices=range(1, 151),
        type=int,
        help='number of vehicles (default: 50)'
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
        '-t', '--time-step',
        metavar='T',
        type=float,
        help='amount of simulated time per step (seconds), or 0 for variable time step; set synch mode unless 0 or --asynch is set'
    )
    argparser.add_argument(
        '--asynch',
        action='store_true',
        help='run in asynch mode, considered less reliable'
    )
    argparser.add_argument(
        '-r', '--rendering',
        type=yes_no,
        help='use rendering mode (y/n)'
    )
    argparser.add_argument(
        '-w', '--wireless-chargers',
        type=argparse.FileType('r'),
        help='CSV file to read wireless charging data from'
    )
    args = argparser.parse_args()

    actor_list = []

    settings = None
    traffic_manager = None
    camera = None
    trackers = None

    try:
        client = carla.Client('127.0.0.1', 2000)
        client.set_timeout(20.0)

        world = None
        if args.map is None:
            world = client.get_world()
        else:
            available_maps = [path.split('/')[-1] for path in client.get_available_maps()]
            if args.map == "list":
                print(available_maps)
                return
            elif args.map in available_maps:
                world = client.load_world(args.map)
            else:
                print("Error: This map is not available.")
                return

        # Set traffic manager to normal speed (140% instead of default 70%). 
        # This kicks the default speed up to about 25 mph.
        traffic_manager = client.get_trafficmanager()
        traffic_manager.global_percentage_speed_difference(-40)

        settings = world.get_settings()
        if args.time_step is not None:
            settings.fixed_delta_seconds = args.time_step
            if args.time_step == 0:
                args.asynch = True
            settings.synchronous_mode = not args.asynch
            world.apply_settings(settings)
            traffic_manager.set_synchronous_mode(not args.asynch)
        if args.rendering is not None:
            settings.no_rendering_mode = not args.rendering
            world.apply_settings(settings)

        blueprint_library = world.get_blueprint_library()

        bp = blueprint_library.find('vehicle.tesla.model3')

        # if bp.has_attribute('color'):
        #     recommended_colors = bp.get_attribute('color').recommended_values
        #     print(f"Recommended colors: {recommended_colors}")
        #     color = random.choice(recommended_colors)
        #     bp.set_attribute('color', color)
        bp.set_attribute('color', '204,255,11') # Lime green to make it visible

        bp.set_attribute('role_name', 'hero')
        traffic_manager.set_hybrid_physics_mode(True)
        traffic_manager.set_respawn_dormant_vehicles(True)

        map = world.get_map()
        spawn_points = map.get_spawn_points()
        if args.spawn_point is None:
            ego_transform = random.choice(spawn_points)
        else:
            choice_location = carla.Location(args.spawn_point[0], args.spawn_point[1], args.spawn_point[2])
            ego_transform = sorted(spawn_points, key=lambda point: point.location.distance(choice_location))[0]
        vehicle = world.spawn_actor(bp, ego_transform)

        actor_list.append(vehicle)
        print(f'created {vehicle.type_id} at {ego_transform.location}')

        physics_vehicle = vehicle.get_physics_control()
        mass = physics_vehicle.mass
        print(f"Mass: {mass} kg")
        # https://arxiv.org/pdf/1908.08920.pdf%5D pg17
        drag = 0.23
        frontal_area = 2.22
        ev = EV(vehicle, capacity=50.0, A_f=frontal_area, C_D=drag)

        vehicle.set_autopilot(True)

        # # Let's add now a "depth" camera attached to the vehicle. Note that the
        # # transform we give here is now relative to the vehicle.
        # camera_bp = blueprint_library.find('sensor.camera.depth')
        # camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        # camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        # actor_list.append(camera)
        # print('created %s' % camera.type_id)

        # # Now we register the function that will be called each time the sensor
        # # receives an image. In this example we are saving the image to disk
        # # converting the pixels to gray-scale.
        # cc = carla.ColorConverter.LogarithmicDepth
        # camera.listen(lambda image: image.save_to_disk('_out/%06d.png' % image.frame, cc))

        for _ in range(args.number_of_vehicles-1):
            bp = random.choice(blueprint_library.filter('vehicle'))

            for _ in range(5):  # Try spawning 5 times
                transform = random.choice(world.get_map().get_spawn_points())
                npc = world.try_spawn_actor(bp, transform)
                if npc is not None:
                    actor_list.append(npc)
                    npc.set_autopilot(True)
                    break
        print(f"Total number of vehicles: {len(actor_list)}")

        # chargers = [
        #     # Charger(carla.Transform(carla.Location(0,0,0), carla.Rotation()), carla.Vector3D(5,1,100)), # Wireless charger at origin with 10m length, 2m width
        #     Charger(ego_transform, carla.Vector3D(10,1,100)), # Wireless charger where vehicle was spawned with 20m length, 2m width
        # ]
        chargers = list()
        if args.wireless_chargers is not None:
            reader = csv.DictReader(args.wireless_chargers)
            for charger in reader:
                location = carla.Location(float(charger['x']), float(charger['y']), float(charger['z']))
                rotation = carla.Rotation(float(charger['pitch']), float(charger['yaw']), float(charger['roll']))
                transform = carla.Transform(location, rotation)
                dimensions = carla.Vector3D(float(charger['width']), float(charger['length']), float(charger['height']))
                chargers.append(Charger(transform, dimensions / 2))

        # The first couple seconds of simulation are less reliable as the vehicles are dropped onto the ground.
        time_tracker = TimeTracker(vehicle)
        time_tracker.start()
        while time_tracker.time < 2:
            if args.asynch:
                world.wait_for_tick()
            else:
                world.tick()

        time_tracker = TimeTracker(vehicle)
        kinematics_tracker = KinematicsTracker(vehicle)
        soc_tracker = SocTracker(ev, hvac=0.0, init_soc=1.0, wireless_chargers=chargers)
        trackers = [time_tracker, kinematics_tracker, soc_tracker]
        for tracker in trackers:
            tracker.start()

        start = time.time()
        t = start
        display_clock = t
        # while t < start + 100:
        # while True:
        while time_tracker.time < 8028:
            if args.asynch:
                world.wait_for_tick()
            else:
                world.tick()
            t = time.time()

            if t - display_clock > 1:
                print(f"After {time_tracker.time:G} s:")
                print(f"\tLocation: {vehicle.get_location()}")
                print(f"\tDistance travelled: {kinematics_tracker.distance_travelled:G} m")
                m_per_s = kinematics_tracker.distance_travelled / time_tracker.time
                km_per_h = m_per_s * 60 * 60 / 1000
                mph = km_per_h / 1.60934
                print(f"\tAverage speed: {m_per_s:G} m/s ({km_per_h:G} km/h) ({mph:G} mph)")
                print(f"\tSpeed: {kinematics_tracker.speed} m/s")
                print(f"\tAcceleration: {kinematics_tracker.acceleration} m/s^2")
                print(f"\tEnergy consumed: {soc_tracker.total_energy:G} kWh")
                kWh_per_m = soc_tracker.total_energy / kinematics_tracker.distance_travelled
                kWh_per_100km = kWh_per_m * 1000 * 100
                kWh_per_100mi = kWh_per_100km * 1.60934
                print(f"\tEnergy efficiency: {kWh_per_m:G} kWh/m ({kWh_per_100km:G} kWh / 100 km) ({kWh_per_100mi:G} kWh / 100 mi)")
                print(f"\tState of charge: {soc_tracker.soc*100:.2f}%")
                display_clock = t

        print(f'Finished in {t-start} seconds.')
        raise KeyboardInterrupt

    except KeyboardInterrupt:
        for tracker in trackers:
            tracker.stop()

        # Note that these plots may throw exceptions if different trackers had different amounts of updates. 
        # This can be avoided via synchronous mode.

        fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, layout='constrained')

        power_plot = plot_power(ax1, time_tracker.time_series, soc_tracker.power_series)

        # Plot speed over time
        speed_ax = ax1.twinx()
        speed_plot, = speed_ax.plot(time_tracker.time_series, kinematics_tracker.speed_series, "g-", label="Speed")
        speed_ax.set_ylabel("Vehicle Speed (m/s)")
        speed_ax.yaxis.label.set_color(speed_plot.get_color())
        speed_ax.tick_params(axis='y', colors=speed_plot.get_color())
        ax1.legend(handles=[power_plot, speed_plot])

        power_plot = plot_power(ax2, time_tracker.time_series, soc_tracker.power_series)

        # Plot acceleration over time
        acceleration_ax = ax2.twinx()
        acceleration_plot, = acceleration_ax.plot(time_tracker.time_series, kinematics_tracker.acceleration_series, "b-", label="Acceleration")
        acceleration_ax.set_ylabel("Vehicle Acceleration (m/s^2)")
        acceleration_ax.yaxis.label.set_color(acceleration_plot.get_color())
        acceleration_ax.tick_params(axis='y', colors=acceleration_plot.get_color())
        ax2.legend(handles=[power_plot, acceleration_plot])

        power_plot = plot_power(ax3, time_tracker.time_series, soc_tracker.power_series)

        # Plot road grade over time
        grade_ax = ax3.twinx()
        grade_plot, = grade_ax.plot(time_tracker.time_series, kinematics_tracker.grade_series, "c-", label="Grade")
        grade_ax.set_ylabel("Road Grade")
        grade_ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
        grade_ax.yaxis.label.set_color(grade_plot.get_color())
        grade_ax.tick_params(axis='y', colors=grade_plot.get_color())
        ax3.legend(handles=[power_plot, grade_plot])

        plt.show()

        # Plot heatmap
        xs = [loc.x for loc in kinematics_tracker.location_series]
        ys = [loc.y for loc in kinematics_tracker.location_series]
        # Make about one square per 2 m
        xrange = max(xs) - min(xs)
        xbins = math.ceil(xrange / 2)
        yrange = max(ys) - min(ys)
        ybins = math.ceil(yrange / 2)
        fig, (ax1, ax2) = plt.subplots(ncols=2, layout='constrained')

        ax1.hexbin(xs, ys, gridsize=xbins)
        ax1.invert_yaxis()
        ax1.set_aspect('equal', adjustable='box')
        ax1.set_title('Vehicle Presence on Map')

        ax2.hist2d(xs, ys, bins=(xbins,ybins))
        ax2.invert_yaxis()
        ax2.set_aspect('equal', adjustable='box')
        ax2.set_title('Vehicle Presence on Map')

        plt.show()

    finally:
        if trackers is not None:
            del trackers

        if not args.asynch and settings is not None:
            settings.synchronous_mode = False
            world.apply_settings(settings)
            traffic_manager.set_synchronous_mode(False)

        if camera is not None:
            camera.destroy()
        if len(actor_list) > 0:
            print('destroying actors')
            client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
            print('done.')

def yes_no(string: str):
    string = string.lower()
    if string in ('y', 'yes', 'true'):
        return True
    if string in ('n', 'no', 'false'):
        return False
    return None

def plot_power(ax, time_series, power_series):
    """
    Plot power over time.
    Returns the plot.
    """
    plot, = ax.plot(time_series, power_series, "r-", label="Power")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Power from Motor (W)")
    ax.yaxis.label.set_color(plot.get_color())
    ax.tick_params(axis='y', colors=plot.get_color())
    return plot


if __name__ == '__main__':

    main()
