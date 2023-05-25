from carla import Vehicle, WorldSnapshot

from tracker import Tracker


class TimeTracker(Tracker):
    def __init__(self, vehicle: Vehicle) -> None:
        super().__init__(vehicle)
        self.time = 0
        self.time_series = list()
        self.interval_series = list()

    def _update(self, snapshot:WorldSnapshot, vehicle) -> None:
        dt = snapshot.delta_seconds
        self.time += dt
        self.time_series.append(self.time)
        self.interval_series.append(dt)
