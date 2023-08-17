import math
from carla import WorldSnapshot, Vector3D
# import sys

from .tracker import Tracker
from .ev import EV


class EnergyTracker(Tracker):
    def __init__(self, ev:EV, hvac:float=0.0) -> None:
        """
        `hvac`: Power used for HVAC, in Watts.
        """
        super().__init__(ev.vehicle)
        self.ev = ev
        self.hvac = hvac

        self.total_energy = 0
        self.power_series = list()  # No, this is not calculus

    def _update(self, snapshot:WorldSnapshot, vehicle) -> None:
        power = self.power(vehicle)
        self.power_series.append(power)
        energy = self.energy_from_power(power, snapshot.delta_seconds)
        self.total_energy += energy

    @staticmethod
    def energy_from_power(power:float, dt:float):
        """
        Return the energy used in kWh.
        `power`: Power in Watts.
        `dt`: Time interval in s.
        """
        kilowatt = power / 1000
        energy = kilowatt * dt / 3600
        return energy

    def power(self, vehicle):
        """
        Return the power used by the motor in Watts.
        """
        acceleration = vehicle.get_acceleration()
        velocity = vehicle.get_velocity()
        speed = math.sqrt(velocity.x ** 2 + velocity.y ** 2)
        if speed > 0:
            # Use only acceleration in direction of velocity (magnitude of the projection of [a.x, a.y] onto [v.x, v.y])
            a_mag = self._acceleration_magnitude(acceleration, velocity)

            # Use velocity to calculate road grade. There may be a better way to do this.
            grade_angle = 0   # Default
            # Ensure vehicle is moving, and don't trust instances where vertical movement > horizontal
            if speed > 0.555556 and abs(velocity.z) < speed:
                grade_angle = math.atan(velocity.z / speed)

            wheel_power = self._wheel_power(a_mag, speed, grade_angle)
            if wheel_power >= 0:
                traction_power = wheel_power / self.ev.motor_to_wheels_efficiency
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
        term1 = self.ev.mass * acceleration
        term2 = self.ev.term2_constants * math.cos(theta) * (self.ev.c_1 * velocity + self.ev.c_2)
        term3 = self.ev.term3_constants * (velocity ** 2)
        term4 = self.ev.mg * math.sin(theta)
        return (term1 + term2 + term3 + term4) * velocity

    def _braking_efficiency(self, acceleration:float):
        """
        Calculate the braking efficiency for a given acceleration.
        https://doi.org/10.1016/j.apenergy.2016.01.097
        I don't love this method, but I have yet to find a better way.
        """
        if acceleration >= 0:
            # print(f"In braking_efficiency: Rejecting nonnegative {acceleration=}.", file=sys.stderr)
            return 0
        exponent = -self.ev.braking_alpha/acceleration
        try:
            denominator = math.e**exponent
        except OverflowError:
            # print(f"In braking_efficiency: {exponent=} caused OverflowError. Returning 0.", file=sys.stderr)
            return 0
        return 1 / denominator
