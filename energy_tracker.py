import math
from carla import Vehicle, WorldSnapshot, Vector3D


class EnergyTracker:
    def __init__(self, vehicle:Vehicle, A_f:float=2.3316,
                gravity:float=9.8066, C_r:float=1.75, c_1:float=0.0328, c_2:float=4.575, 
                rho_Air:float=1.2256, C_D:float=0.28) -> None:
        self.vehicle_id = vehicle.id
        physics_vehicle = vehicle.get_physics_control()
        self.mass = physics_vehicle.mass
        self.A_f = A_f
        self.gravity = gravity
        self.C_r = C_r
        self.c_1 = c_1
        self.c_2 = c_2
        self.rho_Air = rho_Air
        self.C_D = C_D

        self.total_energy = 0
        self.world = vehicle.get_world()
        # self.last_snapshot = self.world.get_snapshot()
        self.world.on_tick(self.on_tick)

    def on_tick(self, snapshot:WorldSnapshot):
        vehicle = snapshot.find(self.vehicle_id)
        power = self.power(vehicle)
        energy = power * snapshot.delta_seconds / (60 * 60)
        self.total_energy += energy
        print(f"Energy consumed: {energy} kWh (Total: {self.total_energy} kWh)")

    def power(self, vehicle):
        acceleration = vehicle.get_acceleration()
        v = vehicle.get_velocity()
        horizontal_v = math.sqrt(v.x ** 2 + v.y ** 2)
        if horizontal_v > 0:
            # Use only acceleration in direction of velocity (magnitude of the projection of [a.x, a.y] onto [v.x, v.y])
            a_mag = self.acceleration_magnitude(acceleration, v)
            if a_mag > 0:
                grade = 0   # Default
                if horizontal_v > 0.555556: # 2 km/h in m/s
                    grade = v.z / horizontal_v
                return self.wheel_power(a_mag, horizontal_v, grade)
            else:
                return 0    # No energy regeneration for now
        else:
            return 0
    
    def acceleration_magnitude(self, acceleration:Vector3D, direction:Vector3D):
        """
        Return the magnitude of the `acceleration` vector in the direction of the `direction` vector.
        """
        dot = acceleration.x*direction.x + acceleration.y*direction.y   # Dot product
        d_mag = math.sqrt(direction.x**2 + direction.y**2)
        return dot / d_mag

    def wheel_power(self, acceleration:float, velocity:float, theta:float):
        term1 = self.mass * acceleration
        term2 = self.mass * self.gravity * math.cos(theta) * self.C_r * (self.c_1 * velocity + self.c_2) / 1000
        term3 = self.rho_Air * self.A_f * self.C_D * (velocity ** 2) / 2
        term4 = self.mass * self.gravity * math.sin(theta)
        return (term1 + term2 + term3 + term4) * velocity
