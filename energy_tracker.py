import math
from carla import Vehicle, WorldSnapshot, Vector3D
import sys

from tracker import Tracker


class EnergyTracker(Tracker):
    def __init__(self, vehicle:Vehicle, hvac:float=0, A_f:float=2.3316,
                gravity:float=9.8066, C_r:float=1.75, c_1:float=0.0328, c_2:float=4.575, 
                rho_Air:float=1.2256, C_D:float=0.28,
                motor_efficiency:float=0.91, driveline_efficiency:float=0.92, 
                braking_alpha:float=0.0411) -> None:
        """
        `hvac`: Power used for HVAC, in Watts.
        The remaining values are from https://doi.org/10.1016/j.apenergy.2016.01.097 .
        """
        super().__init__(vehicle)
        physics_vehicle = vehicle.get_physics_control()
        self.mass = physics_vehicle.mass
        self.hvac = hvac
        self.A_f = A_f
        self.gravity = gravity
        self.C_r = C_r
        self.c_1 = c_1
        self.c_2 = c_2
        self.rho_Air = rho_Air
        self.C_D = C_D
        self.motor_to_wheels_efficiency = motor_efficiency * driveline_efficiency
        self.braking_alpha = braking_alpha

        self.total_energy = 0
        self.power_series = list()  # No, this is not calculus

    def _update(self, snapshot:WorldSnapshot, vehicle) -> None:
        power = self.power(vehicle)
        self.power_series.append(power)
        energy = self.energy_from_power(power, snapshot.delta_seconds)
        self.total_energy += energy

    def energy_from_power(self, power:float, dt:float):
        """
        Return the energy used in kWh.
        `power`: Power in Watts.
        `dt`: Time interval in s.
        """
        kilowatt = power / 1000
        energy = kilowatt * dt / (60 * 60)
        return energy

    def power(self, vehicle):
        """
        Return the power used by the motor in Watts.
        """
        acceleration = vehicle.get_acceleration()
        v = vehicle.get_velocity()
        horizontal_v = math.sqrt(v.x ** 2 + v.y ** 2)
        if horizontal_v > 0:
            # Use only acceleration in direction of velocity (magnitude of the projection of [a.x, a.y] onto [v.x, v.y])
            a_mag = self._acceleration_magnitude(acceleration, v)
            grade = 0   # Default
            if horizontal_v > 0.555556: # 2 km/h in m/s
                grade = v.z / horizontal_v  # Use velocity to calculate road grade. There may be a better way to do this.
            wheel_power = self._wheel_power(a_mag, horizontal_v, grade)
            if wheel_power >= 0:
                traction_power = wheel_power / (self.motor_to_wheels_efficiency)
            else:
                traction_power = wheel_power * self._braking_efficiency(a_mag)
            return traction_power + self.hvac
        else:
            return self.hvac
    
    def _acceleration_magnitude(self, acceleration:Vector3D, direction:Vector3D):
        """
        Return the magnitude of the `acceleration` vector in the direction of the `direction` vector.
        """
        dot = acceleration.x*direction.x + acceleration.y*direction.y   # Dot product
        direction_magnitude = math.sqrt(direction.x**2 + direction.y**2)
        return dot / direction_magnitude

    def _wheel_power(self, acceleration:float, velocity:float, theta:float):
        """
        Calculate the power at the wheels in Watts.
        https://doi.org/10.1016/j.apenergy.2016.01.097
        """
        term1 = self.mass * acceleration
        term2 = self.mass * self.gravity * math.cos(theta) * self.C_r * (self.c_1 * velocity + self.c_2) / 1000
        term3 = self.rho_Air * self.A_f * self.C_D * (velocity ** 2) / 2
        term4 = self.mass * self.gravity * math.sin(theta)
        return (term1 + term2 + term3 + term4) * velocity
    
    def _braking_efficiency(self, acceleration:float):
        """
        Calculate the braking efficiency for a given acceleration.
        https://doi.org/10.1016/j.apenergy.2016.01.097
        I don't love this method, but I have yet to find a better way.
        """
        if acceleration >= 0:
            print(f"In braking_efficiency: Rejecting nonnegative {acceleration=}.", file=sys.stderr)
            return 0
        exponent = -self.braking_alpha/acceleration
        try:
            denominator = math.e**exponent
        except OverflowError:
            print(f"In braking_efficiency: {exponent=} caused OverflowError. Returning 0.", file=sys.stderr)
            return 0
        return 1 / denominator
