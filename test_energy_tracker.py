import traceback
from carla import Vehicle, VehiclePhysicsControl, World, WorldSnapshot, Vector3D

from energy_tracker import EnergyTracker


class TestVehicle:
    def __init__(self, acceleration:Vector3D=Vector3D(), velocity:Vector3D=Vector3D()) -> None:
        self.__acceleration = acceleration
        self.__velocity = velocity

    def get_acceleration(self):
        return self.__acceleration

    def get_velocity(self):
        return self.__velocity


class TestEnergyTracker(EnergyTracker):
    def __init__(self, vehicle:Vehicle, A_f:float=2.3316,
                gravity:float=9.8066, C_r:float=1.75, c_1:float=0.0328, c_2:float=4.575, 
                rho_Air:float=1.2256, C_D:float=0.28,
                motor_efficiency:float=0.91, driveline_efficiency:float=0.92, 
                braking_alpha:float=0.0411, mass=1521) -> None:
        self.mass = mass
        self.A_f = A_f
        self.gravity = gravity
        self.C_r = C_r
        self.c_1 = c_1
        self.c_2 = c_2
        self.rho_Air = rho_Air
        self.C_D = C_D
        self.motor_to_wheels_efficiency = motor_efficiency * driveline_efficiency
        self.braking_alpha = braking_alpha

    def __del__(self):
        pass


def test_power_1():
    vehicle = TestVehicle()
    tracker = TestEnergyTracker(vehicle)
    power = tracker.power(vehicle)
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
    tracker = TestEnergyTracker(vehicle)
    power = tracker.power(vehicle)
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
    tracker = TestEnergyTracker(vehicle, A_f=4.0)
    power = tracker.power(vehicle)
    try:
        assert power > 1961.2
        assert power < 1961.3
    except AssertionError:
        traceback.print_exc()
        print(f"{power=}")
        print()
        return False
    return True


if __name__ == "__main__":
    success = 0
    total = 0
    for test in (test_power_1, test_power_2, test_power_3):
        if test():
            success += 1
        total += 1
    print(f"Passed {success} out of {total} tests.")
