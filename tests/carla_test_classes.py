from carla import Vector3D


"""
Classes that mimic those of the CARLA simulator without having to run it.
"""


class TestVehicle:
    class PhysicsControl:
        def __init__(self) -> None:
            self.mass = 1521

    def __init__(self, acceleration:Vector3D=Vector3D(), velocity:Vector3D=Vector3D()) -> None:
        self.__acceleration = acceleration
        self.__velocity = velocity

    def get_physics_control(self):
        return self.PhysicsControl()

    def get_acceleration(self):
        return self.__acceleration

    def get_velocity(self):
        return self.__velocity

