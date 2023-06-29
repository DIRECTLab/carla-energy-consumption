import sys
import os
import traceback
from carla import Vector3D, Rotation, Transform

from carla_test_classes import TestVehicle

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trackers.soc_tracker import SocTracker
from trackers.ev import EV
from trackers.charger import Charger


"""
This module tests the state of charge functionality of `SocTracker`.
"""


def test_soc1():
    vehicle = TestVehicle()
    world = vehicle.get_world()
    ev = EV(vehicle, capacity=50.0)
    tracker = SocTracker(ev)
    tracker.start()
    world.tick()
    try:
        assert tracker.soc == 1.0
    except AssertionError:
        traceback.print_exc()
        print(f"{tracker.soc=}")
        print()
        return False
    return True


def test_soc2():
    vehicle = TestVehicle()
    world = vehicle.get_world()
    ev = EV(vehicle, capacity=50.0)
    tracker = SocTracker(ev, hvac=1000)
    tracker.start()
    world.tick()
    try:
        assert tracker.soc > 0.9799
        assert tracker.soc < 0.9801
    except AssertionError:
        traceback.print_exc()
        print(f"{tracker.soc=}")
        print()
        return False
    return True


def test_soc3():
    """
    SOC cannot exceed 100%
    """
    vehicle = TestVehicle()
    world = vehicle.get_world()
    ev = EV(vehicle, capacity=50.0)
    tracker = SocTracker(ev, hvac=-1000)
    tracker.start()
    world.tick()
    try:
        assert tracker.soc == 1.0
    except AssertionError:
        traceback.print_exc()
        print(f"{tracker.soc=}")
        print()
        return False
    return True


def test_wireless1():
    vehicle = TestVehicle()
    world = vehicle.get_world()
    ev = EV(vehicle, capacity=200.0)
    charger = Charger(
        transform=Transform(Vector3D(), Rotation()), 
        extent=Vector3D(1,1,1)
    )
    tracker = SocTracker(ev, init_soc=0.0, wireless_chargers=[charger])
    tracker.start()
    world.tick()
    try:
        assert tracker.is_charging
        assert tracker.soc == 0.5
    except AssertionError:
        traceback.print_exc()
        print(f"{tracker.soc=}")
        print()
        return False
    return True


def test_wireless2():
    vehicle = TestVehicle()
    world = vehicle.get_world()
    ev = EV(vehicle, capacity=200.0)
    charger1 = Charger(
        transform=Transform(Vector3D(), Rotation()), 
        extent=Vector3D(1,1,1)
    )
    charger2 = Charger(
        transform=Transform(Vector3D(2,2,2), Rotation()), 
        extent=Vector3D(1,1,1)
    )
    tracker = SocTracker(ev, init_soc=0.0, wireless_chargers=[charger1, charger2])
    tracker.start()
    world.tick()
    try:
        assert tracker.is_charging
        assert tracker.soc == 0.5
    except AssertionError:
        traceback.print_exc()
        print(f"{tracker.soc=}")
        print()
        return False
    return True


if __name__ == '__main__':
    tests = (
        test_soc1,
        test_soc2,
        test_soc3,
        test_wireless1,
        test_wireless2,
    )
    success = 0
    total = 0
    for test in tests:
        if test():
            success += 1
        total += 1
    print(f"Passed {success} out of {total} tests.")
