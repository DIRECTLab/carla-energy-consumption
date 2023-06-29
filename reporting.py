import pandas as pd

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


def save_data(trackers:list, file):
    if len(trackers) == 0:
        return
    
    data = dict()
    for tracker in trackers:
        if isinstance(tracker, TimeTracker):
            data['time'] = tracker.time_series
            data['dt'] = tracker.interval_series
        elif isinstance(tracker, KinematicsTracker):
            data['location'] = tracker.location_series
            data['speed'] = tracker.speed_series
            data['distance'] = tracker.distance_series
            data['acceleration'] = tracker.acceleration_series
            data['road_grade'] = tracker.grade_series
        elif isinstance(tracker, EnergyTracker):
            data['power'] = tracker.power_series
            if isinstance(tracker, SocTracker):
                data['SOC'] = tracker.soc_series

    pd.DataFrame(data).to_csv(file)
