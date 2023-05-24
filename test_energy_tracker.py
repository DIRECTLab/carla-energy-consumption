from carla import Vehicle, VehiclePhysicsControl, World, WorldSnapshot, Vector3D

from energy_tracker import EnergyTracker


# class TestPhysicsControl(VehiclePhysicsControl):
#     mass = 1521


# class TestSnapshot(WorldSnapshot):
#     pass


# class TestWorld(World):
#     def __init__(self) -> None:
#         self.__callbacks = list()
#         self.__snapshot = TestSnapshot()

#     def on_tick(self, callback):
#         self.__callbacks.append(callback)
#         return len(self.__callbacks) - 1

#     def tick(self):
#         for callback in self.__callbacks:
#             callback(self.__snapshot)

#     def remove_on_tick(self, callback_id):
#         self.__callbacks.pop(callback_id)


class TestVehicle:
    def __init__(self, acceleration:Vector3D=Vector3D(), velocity:Vector3D=Vector3D()) -> None:
        self.__acceleration = acceleration
        self.__velocity = velocity

    def get_acceleration(self):
        return self.__acceleration

    def get_velocity(self):
        return self.__velocity


class TestEnergyTracker(EnergyTracker):
    def __init__(self, vehicle: Vehicle, A_f: float = 2.3316, gravity: float = 9.8066, C_r: float = 1.75, c_1: float = 0.0328, c_2: float = 4.575, rho_Air: float = 1.2256, C_D: float = 0.28, motor_efficiency: float = 0.91, driveline_efficiency: float = 0.92, braking_alpha: float = 0.0411) -> None:
        pass

    def __del__(self):
        pass


def test_power_1():
    vehicle = TestVehicle()
    tracker = TestEnergyTracker(vehicle)
    power = tracker.power(vehicle)
    assert power == 0


# def test_power_2():
#     vehicle = TestVehicle()
#     tracker = TestEnergyTracker(vehicle)
#     power = tracker.power(vehicle)
#     assert power == 0


if __name__ == "__main__":
    test_power_1()
