import sys
import os
import traceback
from carla import Location

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from interface.trackers.charger import Charger


def test_transform_in1():
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,3,0)
    charger = Charger(front_left, front_right, back_right, 0, 0)
    point = Location(1,0,0)
    transformed = charger.transform_in(point)
    try:
        assert transformed == Location(1.5, -1.5, 0.0)
    except AssertionError:
        traceback.print_exc()
        print(f"transformed=({transformed.x}, {transformed.y}, {transformed.z})")
        print()
        return False
    return True


def test_transform_in2():
    front_left = Location(0,-1,0)
    front_right = Location(0,0,0)
    back_right = Location(-3,0,0)
    charger = Charger(front_left, front_right, back_right, 0, 0)
    point = Location(1,0,0)
    transformed = charger.transform_in(point)
    try:
        assert transformed == Location(0.5, -2.5, 0.0)
    except AssertionError:
        traceback.print_exc()
        print(f"transformed=({transformed.x}, {transformed.y}, {transformed.z})")
        print()
        return False
    return True


def test_transform_in3():
    front_left = Location(0,-1,0)
    front_right = Location(0,0,0)
    back_right = Location(-3,0,0)
    charger = Charger(front_left, front_right, back_right, 0, 0)
    point = Location(0,1,1)
    transformed = charger.transform_in(point)
    try:
        assert transformed == Location(1.5, -1.5, 1.0)
    except AssertionError:
        traceback.print_exc()
        print(f"transformed=({transformed.x}, {transformed.y}, {transformed.z})")
        print()
        return False
    return True


def test_transform_in4():
    # Rotated 45 degrees
    front_left = Location(0, -1, 0)
    front_right = Location(1, 0, 0)
    back_right = Location(0, 1, 0)
    charger = Charger(front_left, front_right, back_right, 0, 0)
    point = Location(-1, 0, 0)   # the missing corner
    transformed = charger.transform_in(point)
    try:
        assert transformed.distance(Location(-0.70710678, 0.70710678, 0.0)) < 0.0001
    except AssertionError:
        traceback.print_exc()
        print(f"transformed=({transformed.x}, {transformed.y}, {transformed.z})")
        print()
        return False
    return True


def test_transform_in5():
    # Length=2, width=2, 30% grade
    # I don't know for sure, but I think this is an accuracy problem
    front_left = Location(-0.977241014286, -0.977241014286, 0.3)
    front_right = Location(0.977241014286, -0.977241014286, 0.3)
    back_right = Location(0.977241014286, 0.977241014286, -0.3)
    charger = Charger(front_left, front_right, back_right, 0, 0)
    point = Location(-0.977241014286, 0.977241014286, -0.3)   # the missing corner
    transformed = charger.transform_in(point)
    try:
        assert transformed.distance(Location(-1.0, 1.0, 0.0)) < 0.01
    except AssertionError:
        traceback.print_exc()
        print(f"transformed=({transformed.x}, {transformed.y}, {transformed.z})")
        print()
        return False
    return True


def test_transform_in6():
    # Length=2, width=2, 30% grade rotated 45 degrees
    # I don't know for sure, but I think this is an accuracy problem
    front_left = Location(0, -1.38202749611, 0.3)
    front_right = Location(1.38202749611, 0, 0.3)
    back_right = Location(0, 1.38202749611, -0.3)
    charger = Charger(front_left, front_right, back_right, 0, 0)
    point = Location(-1.38202749611, 0, -0.3)   # the missing corner
    transformed = charger.transform_in(point)
    try:
        assert transformed.distance(Location(-1.0, 1.0, 0.0)) < 0.01
    except AssertionError:
        traceback.print_exc()
        print(f"transformed=({transformed.x}, {transformed.y}, {transformed.z})")
        print()
        return False
    return True


def test_power_to_vehicle1():
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,3,0)
    charger = Charger(front_left, front_right, back_right, 0, 0.85)
    point = Location(-0.5,1.5,0)
    power = charger.power_to_vehicle(point)
    try:
        assert power == 0.0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_to_vehicle2():
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,3,0)
    charger = Charger(front_left, front_right, back_right, 30_000, 0)
    point = Location(-0.5,1.5,0)
    power = charger.power_to_vehicle(point)
    try:
        assert power == 0.0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_to_vehicle3():
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,3,0)
    charger = Charger(front_left, front_right, back_right, 30_000, 0.85)
    point = Location(-1,1.5,0)
    power = charger.power_to_vehicle(point)
    try:
        assert power == 0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_to_vehicle4():
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,3,0)
    charger = Charger(front_left, front_right, back_right, 30_000, 0.85)
    point = Location(-0.5,1.5,0)
    power = charger.power_to_vehicle(point)
    try:
        assert power == 25_500.0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_to_vehicle5():
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,3,0)
    charger = Charger(front_left, front_right, back_right, 30_000, 0.85)
    point = Location(-0.25,1.5,0)
    power = charger.power_to_vehicle(point)
    try:
        assert power == 19_125.0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


# TODO: Test power when charger is tilted


if __name__ == "__main__":
    tests = (
        test_transform_in1,
        test_transform_in2,
        test_transform_in3,
        test_transform_in4,
        test_transform_in5,
        test_transform_in6,
        test_power_to_vehicle1,
        test_power_to_vehicle2,
        test_power_to_vehicle3,
        test_power_to_vehicle4,
        test_power_to_vehicle5,
    )
    success = 0
    total = 0
    for test in tests:
        if test():
            success += 1
        total += 1
    print(f"Passed {success} out of {total} tests.")
