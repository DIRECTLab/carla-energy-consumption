from carla import Vehicle, WorldSnapshot


from tracker import Tracker


class KinematicsTracker(Tracker):
    def __init__(self, vehicle: Vehicle) -> None:
        super().__init__(vehicle)
        self.speed_series = list()
        self.acceleration_series = list()

    def _update(self, snapshot: WorldSnapshot, vehicle) -> None:
        velocity = vehicle.get_velocity()
        speed = velocity.length()
        self.speed_series.append(speed)

        if speed != 0:
            acceleration = vehicle.get_acceleration()
            dot = velocity.dot_2d(acceleration)
            acceleration_magnitude = dot / speed
        else:
            acceleration_magnitude = 0  # This is a pretty safe assumption
        self.acceleration_series.append(acceleration_magnitude)
