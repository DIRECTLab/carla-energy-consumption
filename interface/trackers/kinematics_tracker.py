import math
from threading import Lock
from carla import Vehicle, WorldSnapshot


from .tracker import Tracker


class KinematicsTracker(Tracker):
    def __init__(self, vehicle: Vehicle) -> None:
        super().__init__(vehicle)
        self.init_time = vehicle.get_world().get_snapshot().elapsed_seconds
        self.elapsed_time = 0
        self.time_series = list()
        self.location_series = list()
        self.speed_series = list()
        self.distance_travelled = 0
        self.distance_series = list()
        self.acceleration_series = list()
        self.grade_series = list()

        self.update_lock = Lock()

    def _update(self, snapshot: WorldSnapshot, vehicle) -> None:
        with self.update_lock:
            self.elapsed_time = snapshot.elapsed_seconds - self.init_time
            self.time_series.append(snapshot.elapsed_seconds)
            self.location_series.append(vehicle.get_transform().location)

            velocity = vehicle.get_velocity()
            speed = math.sqrt(velocity.x ** 2 + velocity.y ** 2)
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
            self.acceleration_series.append(acceleration_magnitude)

            # Derive road grade from velocity
            grade = 0
            # Ensure vehicle is moving, and don't trust instances where vertical movement > horizontal
            if speed > 0.555556 and abs(velocity.z) < speed:
                grade = velocity.z / speed
            self.grade_series.append(grade)
