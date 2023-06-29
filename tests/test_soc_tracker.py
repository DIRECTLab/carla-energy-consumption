import sys
import os
import traceback
from carla import Vector3D

from carla_test_classes import TestVehicle

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trackers.soc_tracker import SocTracker
from trackers.ev import EV


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
    tracker.stop()
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
    tracker.stop()
    try:
        assert tracker.soc > 0.9999944
        assert tracker.soc < 0.9999945
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
    )
    success = 0
    total = 0
    for test in tests:
        if test():
            success += 1
        total += 1
    print(f"Passed {success} out of {total} tests.")
