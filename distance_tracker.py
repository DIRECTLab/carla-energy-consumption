from carla import Vehicle, WorldSnapshot
import math

from tracker import Tracker


class DistanceTracker(Tracker):
    def __init__(self, vehicle:Vehicle) -> None:
        super().__init__(vehicle)
        self.distance_travelled = 0

    def _on_tick(self, snapshot:WorldSnapshot):
        vehicle = super()._on_tick(snapshot)
        if vehicle is not None:
            velocity = vehicle.get_velocity()
            horizontal_v = math.sqrt(velocity.x ** 2 + velocity.y ** 2)
            distance = horizontal_v * snapshot.delta_seconds
            if distance != 0:
                self.distance_travelled += distance
        return vehicle
