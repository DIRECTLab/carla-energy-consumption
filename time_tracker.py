from carla import Vehicle, WorldSnapshot
import math
import sys

from tracker import Tracker


class TimeTracker(Tracker):
    def __init__(self, vehicle: Vehicle) -> None:
        super().__init__(vehicle)
        self.time = 0

    def _on_tick(self, snapshot:WorldSnapshot):
        vehicle = super()._on_tick(snapshot)
        if vehicle is not None:
            self.time += snapshot.delta_seconds
        return vehicle
