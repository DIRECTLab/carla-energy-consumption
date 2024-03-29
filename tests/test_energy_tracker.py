import sys
import os
import traceback
from carla import Vector3D

from carla_test_classes import TestVehicle

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from interface.trackers.energy_tracker import EnergyTracker
from interface.trackers.ev import EV


def test_power_1():
    vehicle = TestVehicle()
    ev = EV(vehicle, capacity=50)
    tracker = EnergyTracker(ev)
    power = tracker.power(vehicle.snapshot)
    try:
        assert power == 0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_2():
    vehicle = TestVehicle(Vector3D(1, 0, 0), Vector3D(1, 0, 0))
    ev = EV(vehicle, capacity=50)
    tracker = EnergyTracker(ev)
    power = tracker.power(vehicle.snapshot)
    try:
        assert power > 1960.9
        assert power < 1961.0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_3():
    vehicle = TestVehicle(Vector3D(1, 0, 0), Vector3D(1, 0, 0))
    ev = EV(vehicle, capacity=50, A_f=4.0)
    tracker = EnergyTracker(ev)
    power = tracker.power(vehicle.snapshot)
    try:
        assert power > 1961.2
        assert power < 1961.3
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_4():
    vehicle = TestVehicle(Vector3D(1, 0, 0), Vector3D(1, 0, 0))
    ev = EV(vehicle, capacity=50, C_r=2.0)
    tracker = EnergyTracker(ev)
    power = tracker.power(vehicle.snapshot)
    try:
        assert power > 1981.4
        assert power < 1981.5
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_5():
    vehicle = TestVehicle(Vector3D(2, 0, 0), Vector3D(1, 0, 0))
    ev = EV(vehicle, capacity=50)
    tracker = EnergyTracker(ev)
    power = tracker.power(vehicle.snapshot)
    try:
        assert power > 3777.6
        assert power < 3777.7
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_6():
    vehicle = TestVehicle(Vector3D(1, 0, 0), Vector3D(2, 0, 0))
    ev = EV(vehicle, capacity=50)
    tracker = EnergyTracker(ev)
    power = tracker.power(vehicle.snapshot)
    try:
        assert power > 3926.7
        assert power < 3926.8
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_7():
    vehicle = TestVehicle(Vector3D(1, 0, 0), Vector3D(1, 0, 0.1))
    ev = EV(vehicle, capacity=50)
    tracker = EnergyTracker(ev)
    power = tracker.power(vehicle.snapshot)
    try:
        assert power > 3732.9
        assert power < 3733.0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_8():
    vehicle = TestVehicle(Vector3D(-1, 0, 0), Vector3D(1, 0, 0))
    ev = EV(vehicle, capacity=50)
    tracker = EnergyTracker(ev)
    power = tracker.power(vehicle.snapshot)
    try:
        assert power > -1344.0
        assert power < -1343.9
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_9():
    """
    Only use acceleration in the direction of velocity.
    """
    vehicle = TestVehicle(Vector3D(1, 1, 0), Vector3D(1, 0, 0))
    ev = EV(vehicle, capacity=50)
    tracker = EnergyTracker(ev)
    power = tracker.power(vehicle.snapshot)
    try:
        assert power > 1960.9
        assert power < 1961.0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_10():
    """
    Ensure magnitude of velocity is used.
    """
    vehicle = TestVehicle(Vector3D(1, 1, 0), Vector3D(1, 1, 0))
    ev = EV(vehicle, capacity=50)
    tracker = EnergyTracker(ev)
    power = tracker.power(vehicle.snapshot)
    try:
        assert power > 3838.6
        assert power < 3838.7
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_11():
    vehicle = TestVehicle(Vector3D(1, 0, 0), Vector3D(1, 0, 0))
    ev = EV(vehicle, capacity=50)
    tracker = EnergyTracker(ev, hvac=6000)
    power = tracker.power(vehicle.snapshot)
    try:
        assert power > 7960.9
        assert power < 7961.0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True



def test_energy_1():
    energy = EnergyTracker.energy_from_power(0, 1)
    try:
        assert energy == 0
    except AssertionError:
        traceback.print_exc()
        print(f"{energy=}")
        print()
        return False
    return True


def test_energy_2():
    energy = EnergyTracker.energy_from_power(1960.91, 3600)
    try:
        assert energy > 1.9609
        assert energy < 1.9610
    except AssertionError:
        traceback.print_exc()
        print(f"{energy=}")
        print()
        return False
    return True


def test_energy_3():
    energy = EnergyTracker.energy_from_power(-1343.94, 3600)
    try:
        assert energy > -1.3440
        assert energy < -1.3439
    except AssertionError:
        traceback.print_exc()
        print(f"{energy=}")
        print()
        return False
    return True


def test_energy_4():
    energy = EnergyTracker.energy_from_power(1960.91, 1)
    try:
        assert energy > 0.00054469
        assert energy < 0.00054470
    except AssertionError:
        traceback.print_exc()
        print(f"{energy=}")
        print()
        return False
    return True


def test_total_energy():
    vehicle = TestVehicle(Vector3D(1, 0, 0), Vector3D(1, 0, 0))
    world = vehicle.get_world()
    ev = EV(vehicle, capacity=50)
    tracker = EnergyTracker(ev)
    tracker.start()
    world.tick()
    try:
        assert tracker.total_energy > 1.9609
        assert tracker.total_energy < 1.9610
    except AssertionError:
        traceback.print_exc()
        print(f"{tracker.total_energy=}")
        print()
        return False
    return True


if __name__ == "__main__":
    tests = (
        test_power_1, 
        test_power_2, 
        test_power_3, 
        test_power_4, 
        test_power_5, 
        test_power_6, 
        test_power_7,
        test_power_8,
        test_power_9,
        test_power_10,
        test_power_11,
        test_energy_1,
        test_energy_2,
        test_energy_3,
        test_energy_4,
        test_total_energy,
        )
    success = 0
    total = 0
    for test in tests:
        if test():
            success += 1
        total += 1
    print(f"Passed {success} out of {total} tests.")
