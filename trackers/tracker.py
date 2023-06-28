from carla import Vehicle, WorldSnapshot
import sys


class Tracker:
    """
    Abstract class for tracking vehicle info.
    """
    def __init__(self, vehicle:Vehicle) -> None:
        self.vehicle_id = vehicle.id
        self.__world = vehicle.get_world()
        self.__running = False

    def __del__(self) -> None:
        self.stop()

    def start(self):
        if not self.__running:
            self.__on_tick_id = self.__world.on_tick(self.__on_tick)
            self.__running = True

    def stop(self):
        if self.__running:
            self.__world.remove_on_tick(self.__on_tick_id)
            self.__running = False

    def __on_tick(self, snapshot:WorldSnapshot):
        vehicle = snapshot.find(self.vehicle_id)
        if vehicle is None:
            print(f"Error: Dead vehicle {self.vehicle_id}.", file=sys.stderr)
            self.stop()
        else:
            self._update(snapshot, vehicle)
    
    def _update(self, snapshot:WorldSnapshot, vehicle) -> None:
        raise NotImplementedError("Tracker must implement _update().")
