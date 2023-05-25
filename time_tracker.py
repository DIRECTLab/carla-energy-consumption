from carla import Vehicle, WorldSnapshot

from tracker import Tracker


class TimeTracker(Tracker):
    def __init__(self, vehicle: Vehicle) -> None:
        super().__init__(vehicle)
        self.time = 0

    def _update(self, snapshot:WorldSnapshot, vehicle) -> None:
        self.time += snapshot.delta_seconds
