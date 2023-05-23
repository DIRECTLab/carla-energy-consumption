import math
from carla import Vehicle, WorldSnapshot


class EnergyTracker:
    def __init__(self, vehicle:Vehicle, A_f:float=2.3316,
                gravity:float=9.8066, C_r:float=1.75, c_1:float=0.0328, c_2:float=4.575, 
                rho_Air:float=1.2256, C_D:float=0.28) -> None:
        self.vehicle = vehicle
        physics_vehicle = vehicle.get_physics_control()
        self.mass = physics_vehicle.mass
        self.A_f = A_f
        self.gravity = gravity
        self.C_r = C_r
        self.c_1 = c_1
        self.c_2 = c_2
        self.rho_Air = rho_Air
        self.C_D = C_D

    def tick(self):
        print(f"Power consumed: {self.power()} kW")

    def power(self):
        acceleration = self.vehicle.get_acceleration()
        v = self.vehicle.get_velocity()
        if self.check_acceleration(acceleration, v):
            horizontal_a = math.sqrt(acceleration.x**2 + acceleration.y**2)
            # TODO: Use only acceleration in direction of velocity (magnitude of the projection of [a.x, a.y] onto [v.x, v.y])?
            horizontal_v = math.sqrt(v.x ** 2 + v.y ** 2)
            grade = 0   # Default
            if horizontal_v > 0.555556: # 2 km/h in m/s
                grade = v.z / horizontal_v
            return self.wheel_power(horizontal_a, horizontal_v, grade)
        else:
            return 0    # No energy regeneration for now

    def check_acceleration(self, acceleration, velocity):
        """
        Return whether the object is accelerating (not decelerating) relative to the direction of its velocity.
        """
        d = acceleration.x*velocity.x + acceleration.y*velocity.y   # Dot product
        return d > 0

    def wheel_power(self, acceleration:float, velocity:float, theta:float):
        term1 = self.mass * acceleration
        term2 = self.mass * self.gravity * math.cos(theta) * self.C_r * (self.c_1 * velocity + self.c_2) / 1000
        term3 = self.rho_Air * self.A_f * self.C_D * (velocity ** 2) / 2
        term4 = self.mass * self.gravity * math.sin(theta)
        return (term1 + term2 + term3 + term4) * velocity
