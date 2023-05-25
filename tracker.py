from carla import Vehicle, WorldSnapshot
import sys


class Tracker:
    def __init__(self, vehicle:Vehicle) -> None:
        self.vehicle_id = vehicle.id
        self._world = vehicle.get_world()
        self._running = False

    def __del__(self) -> None:
        self.stop()

    def start(self):
        if not self._running:
            self._on_tick_id = self._world.on_tick(self._on_tick)
            self._running = True

    def stop(self):
        if self._running:
            self._world.remove_on_tick(self._on_tick_id)
            self._running = False

    def _on_tick(self, snapshot:WorldSnapshot):
        vehicle = snapshot.find(self.vehicle_id)
        if vehicle is None:
            print(f"Error: Dead vehicle {self.vehicle_id}.", file=sys.stderr)
            self._world.remove_on_tick(self._on_tick_id)
        return vehicle
