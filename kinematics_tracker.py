from carla import Vehicle, WorldSnapshot


from tracker import Tracker


class KinematicsTracker(Tracker):
    def __init__(self, vehicle: Vehicle) -> None:
        super().__init__(vehicle)
        self.speed = 0
        self.speed_series = list()
        self.distance_travelled = 0
        self.distance_series = list()
        self.acceleration = 0
        self.acceleration_series = list()

    def _update(self, snapshot: WorldSnapshot, vehicle) -> None:
        velocity = vehicle.get_velocity()
        speed = velocity.length()
        self.speed = speed
        self.speed_series.append(speed)
        
        distance = speed * snapshot.delta_seconds
        self.distance_travelled += distance
        self.distance_series.append(distance)

        if speed != 0:
            acceleration = vehicle.get_acceleration()
            dot = velocity.dot_2d(acceleration)
            acceleration_magnitude = dot / speed
        else:
            acceleration_magnitude = 0  # This is a pretty safe assumption
        self.acceleration = acceleration_magnitude
        self.acceleration_series.append(acceleration_magnitude)
