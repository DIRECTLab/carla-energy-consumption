import sys
import os
import traceback

from carla_test_classes import TestVehicle

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from interface.supervehicle import SuperVehicle


def test_ev1():
    ev_params = {
        'capacity': 40.0,
    }
    sv = SuperVehicle(TestVehicle(), 'traffic_manager', ev_params, init_soc=1.0)
    try:
        assert sv.capacity == 40.0
        assert sv.A_f == 2.3316
    except AssertionError:
        traceback.print_exc()
        print(f"{sv.capacity=}")
        print(f"{sv.A_f=}")
        print()
        return False
    return True


def test_ev2():
    ev_params = {
        'C_D': 0.23,
        'capacity': 40.0,
    }
    sv = SuperVehicle(TestVehicle(), 'traffic_manager', ev_params, init_soc=1.0)
    try:
        assert sv.capacity == 40.0
        assert sv.C_D == 0.23
    except AssertionError:
        traceback.print_exc()
        print(f"{sv.capacity=}")
        print(f"{sv.C_D=}")
        print()
        return False
    return True


if __name__ == "__main__":
    tests = (
        test_ev1, 
        test_ev2,
    )
    success = 0
    total = 0
    for test in tests:
        if test():
            success += 1
        total += 1
    print(f"Passed {success} out of {total} tests.")
