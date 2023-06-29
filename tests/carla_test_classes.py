from carla import Vector3D, VehiclePhysicsControl


"""
Classes that mimic those of the CARLA simulator without having to run it.

These classes are not comprehensive. Add to them as needed.
"""


class TestWorld:
    """
    Currently only handles one callback at a time
    """
    def __init__(self) -> None:
        # self.__callbacks = list()
        pass

    def on_tick(self, callback):
        # self.__callbacks.append(callback)
        return -1

    def remove_on_tick(self, callback_id):
        # self.__callbacks.clear()
        pass


class TestVehicle:
    def __init__(self, acceleration:Vector3D=Vector3D(), velocity:Vector3D=Vector3D()) -> None:
        self.id = -1
        self.__acceleration = acceleration
        self.__velocity = velocity

    def get_physics_control(self):
        return VehiclePhysicsControl(mass=1521)
    
    def get_world(self):
        return TestWorld()

    def get_acceleration(self):
        return self.__acceleration

    def get_velocity(self):
        return self.__velocity
