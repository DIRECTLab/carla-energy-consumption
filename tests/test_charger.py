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
    front_left = Location(-1, -0.957826285221, 0.287347885566)
    front_right = Location(1, -0.957826285221, 0.287347885566)
    back_right = Location(1, 0.957826285221, -0.287347885566)
    charger = Charger(front_left, front_right, back_right, 0, 0)
    point = Location(-1, 0.957826285221, -0.287347885566)   # the missing corner
    transformed = charger.transform_in(point)
    try:
        assert transformed.distance(Location(-1.0, 1.0, 0.0)) < 0.001
    except AssertionError:
        traceback.print_exc()
        print(f"transformed=({transformed.x}, {transformed.y}, {transformed.z})")
        print(f"{transformed.distance(Location(-1.0, 1.0, 0.0))=}")
        print()
        return False
    return True


def test_transform_in6():
    # Length=2, width=2, 30% grade rotated 45 degrees
    front_left = Location(-1.38439224267, 0.029821319708, 0.287347885566)
    front_right = Location(0.029821319708, -1.38439224267, 0.287347885566)
    back_right = Location(1.38439224267, -0.029821319708, -0.287347885566)
    charger = Charger(front_left, front_right, back_right, 0, 0)
    point = Location(-0.029821319708, 1.38439224267, -0.287347885566)   # the missing corner
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
    """0 power"""
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,2,0)
    charger = Charger(front_left, front_right, back_right, 0, 0.90)
    point = Location(-0.5,1,0)
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
    """0 efficiency"""
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,2,0)
    charger = Charger(front_left, front_right, back_right, 30_000, 0)
    point = Location(-0.5,1,0)
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
    """Corner of charge range"""
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,2,0)
    charger = Charger(front_left, front_right, back_right, 30_000, 0.90)
    point = Location(-1.5,3,0)
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
    """Perfect alignment"""
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,2,0)
    charger = Charger(front_left, front_right, back_right, 30_000, 0.90)
    point = Location(-0.5,1,0)
    power = charger.power_to_vehicle(point)
    try:
        assert power == 27_000.0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_to_vehicle5():
    """Offset from travel axis"""
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,2,0)
    charger = Charger(front_left, front_right, back_right, 30_000, 0.90)
    point = Location(0,1,0)
    power = charger.power_to_vehicle(point)
    try:
        assert power == 20_250.0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_to_vehicle6():
    """Offset from lane width axis"""
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,2,0)
    charger = Charger(front_left, front_right, back_right, 30_000, 0.90)
    point = Location(-0.5,2,0)
    power = charger.power_to_vehicle(point)
    try:
        assert power == 13_500.0
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


def test_power_to_vehicle7():
    """Offset from both axes: receiver aligned with corner of transmitter"""
    front_left = Location(-1,0,0)
    front_right = Location(0,0,0)
    back_right = Location(0,2,0)
    charger = Charger(front_left, front_right, back_right, 30_000, 0.90)
    point = Location(0,0,0)
    power = charger.power_to_vehicle(point)
    try:
        assert power == 10_125.0
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
        test_power_to_vehicle6,
        test_power_to_vehicle7,
    )
    success = 0
    total = 0
    for test in tests:
        if test():
            success += 1
        total += 1
    print(f"Passed {success} out of {total} tests.")
