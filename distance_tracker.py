from carla import Vehicle, WorldSnapshot
import math


class DistanceTracker:
    def __init__(self, vehicle:Vehicle) -> None:
        self.vehicle_id = vehicle.id
        self.distance_travelled = 0
        self.world = vehicle.get_world()
        # self.last_snapshot = self.world.get_snapshot()
        self.on_tick_id = self.world.on_tick(self.on_tick)

    def __del__(self):
        self.world.remove_on_tick(self.on_tick_id)

    def on_tick(self, snapshot:WorldSnapshot):
        vehicle = snapshot.find(self.vehicle_id)
        velocity = vehicle.get_velocity()
        horizontal_v = math.sqrt(velocity.x ** 2 + velocity.y ** 2)
        distance = horizontal_v * snapshot.delta_seconds
        if distance != 0:
            self.distance_travelled += distance
            # print(f"Distance travelled: {self.distance_travelled} m")
