import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

from trackers.time_tracker import TimeTracker
from trackers.kinematics_tracker import KinematicsTracker
from trackers.energy_tracker import EnergyTracker
from trackers.soc_tracker import SocTracker


def print_update(time_tracker:TimeTracker, kinematics_tracker:KinematicsTracker, soc_tracker:SocTracker):
    print(f"After {time_tracker.time:G} s:")
    print(f"\tLocation: {kinematics_tracker.location_series[-1]}")
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
    print(f"\tThe vehicle is {'not ' if not soc_tracker.is_charging else ''}charging.")


def compile_data(trackers:list) -> pd.DataFrame:
    data = dict()
    for tracker in trackers:
        if isinstance(tracker, TimeTracker):
            data['time'] = tracker.time_series
            data['dt'] = tracker.interval_series
        elif isinstance(tracker, KinematicsTracker):
            data['x'] = [loc.x for loc in tracker.location_series]
            data['y'] = [loc.y for loc in tracker.location_series]
            data['z'] = [loc.z for loc in tracker.location_series]
            data['speed'] = tracker.speed_series
            data['distance'] = tracker.distance_series
            data['acceleration'] = tracker.acceleration_series
            data['road_grade'] = tracker.grade_series
        elif isinstance(tracker, EnergyTracker):
            data['power'] = tracker.power_series
            if isinstance(tracker, SocTracker):
                data['SOC'] = tracker.soc_series

    return pd.DataFrame(data)


def save_data(trackers:list, file):
    df = compile_data(trackers)
    df.to_csv(file)


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


def power_plots(tracking_data:pd.DataFrame):
    """
    Plot power against several other variables.

    `tracking_data`: `DataFrame` as returned by `compile_data()` with `TimeTracker`, `KinematicsTracker` and `EnergyTracker` input.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, layout='constrained')

    power_plot = plot_power(ax1, tracking_data['time'], tracking_data['power'])

    # Plot speed over time
    speed_ax = ax1.twinx()
    speed_plot, = speed_ax.plot(tracking_data['time'], tracking_data['speed'], "g-", label="Speed")
    speed_ax.set_ylabel("Vehicle Speed (m/s)")
    speed_ax.yaxis.label.set_color(speed_plot.get_color())
    speed_ax.tick_params(axis='y', colors=speed_plot.get_color())
    ax1.legend(handles=[power_plot, speed_plot])

    power_plot = plot_power(ax2, tracking_data['time'], tracking_data['power'])

    # Plot acceleration over time
    acceleration_ax = ax2.twinx()
    acceleration_plot, = acceleration_ax.plot(tracking_data['time'], tracking_data['acceleration'], "b-", label="Acceleration")
    acceleration_ax.set_ylabel("Vehicle Acceleration (m/s^2)")
    acceleration_ax.yaxis.label.set_color(acceleration_plot.get_color())
    acceleration_ax.tick_params(axis='y', colors=acceleration_plot.get_color())
    ax2.legend(handles=[power_plot, acceleration_plot])

    power_plot = plot_power(ax3, tracking_data['time'], tracking_data['power'])

    # Plot road grade over time
    grade_ax = ax3.twinx()
    grade_plot, = grade_ax.plot(tracking_data['time'], tracking_data['road_grade'], "c-", label="Grade")
    grade_ax.set_ylabel("Road Grade")
    grade_ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    grade_ax.yaxis.label.set_color(grade_plot.get_color())
    grade_ax.tick_params(axis='y', colors=grade_plot.get_color())
    ax3.legend(handles=[power_plot, grade_plot])

    plt.show()


def world_heatmap(tracking_data:pd.DataFrame, unit_size:float=2.0):
    """
    Plot heatmap

    `tracking_data`: `DataFrame` as returned by `compile_data()` with `KinematicsTracker` input.

    `unit_size`: Specifies map granularity. Default is one unit for every 2 meters.
    """
    # Make about one square per 2 m
    xs = tracking_data['x']
    xrange = xs.max() - xs.min()
    xbins = math.ceil(xrange / unit_size)
    ys = tracking_data['y']
    yrange = ys.max() - ys.min()
    ybins = math.ceil(yrange / unit_size)
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
