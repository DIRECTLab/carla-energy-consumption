import math
from threading import Lock
from carla import Vehicle, WorldSnapshot


from .tracker import Tracker


class KinematicsTracker(Tracker):
    def __init__(self, vehicle: Vehicle) -> None:
        super().__init__(vehicle)
        self.location_series = list()
        self.speed = 0
        self.speed_series = list()
        self.distance_travelled = 0
        self.distance_series = list()
        self.acceleration = 0
        self.acceleration_series = list()
        self.road_grade = 0
        self.grade_series = list()
        
        self.update_lock = Lock()

    def _update(self, snapshot: WorldSnapshot, vehicle) -> None:
        with self.update_lock:
            self.location_series.append(vehicle.get_transform().location)

            velocity = vehicle.get_velocity()
            speed = math.sqrt(velocity.x ** 2 + velocity.y ** 2)
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

            # Derive road grade from velocity
            grade = 0
            # Ensure vehicle is moving, and don't trust instances where vertical movement > horizontal
            if speed > 0.555556 and abs(velocity.z) < speed:
                grade = velocity.z / speed
            self.road_grade = grade
            self.grade_series.append(grade)
