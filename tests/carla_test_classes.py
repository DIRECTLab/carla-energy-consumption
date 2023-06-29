from carla import Vector3D, VehiclePhysicsControl, Rotation, Transform


"""
Classes that mimic those of the CARLA simulator without having to run it.

These classes are not comprehensive. Add to them as needed.
"""


class TestWorldSnapshot:
    """
    Currently only handles one vehicle.
    """
    def __init__(self, vehicle) -> None:
        self.delta_seconds = 1.0
        self.__vehicle = vehicle

    def find(self, id):
        return self.__vehicle


class TestWorld:
    """
    Currently only handles one callback at a time and one vehicle.
    """
    def __init__(self, vehicle) -> None:
        self.__callbacks = list()
        self.__snapshot = TestWorldSnapshot(vehicle)

    def on_tick(self, callback):
        self.__callbacks.append(callback)
        return -1

    def remove_on_tick(self, callback_id):
        self.__callbacks.clear()

    def tick(self):
        for callback in self.__callbacks:
            callback(self.__snapshot)


class TestVehicle:

    class ActorSnapshot:
        def __init__(self, id, acceleration, velocity) -> None:
            self.id = id
            self.__acceleration = acceleration
            self.__velocity = velocity

        def get_transform(self):
            return Transform(Vector3D(), Rotation())

        def get_acceleration(self):
            return self.__acceleration

        def get_velocity(self):
            return self.__velocity

    def __init__(self, acceleration:Vector3D=Vector3D(), velocity:Vector3D=Vector3D()) -> None:
        self.id = -1
        self.snapshot = self.ActorSnapshot(self.id, acceleration, velocity)
        self.__world = TestWorld(self.snapshot)

    def get_physics_control(self):
        return VehiclePhysicsControl(mass=1521)

    def get_world(self):
        return self.__world
