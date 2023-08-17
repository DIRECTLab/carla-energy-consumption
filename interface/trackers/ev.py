from carla import Vehicle


class EV:
    """
    Data class with static electric vehicle info.
    """

    def __init__(self, vehicle:Vehicle, capacity:float, A_f:float=2.3316,
                gravity:float=9.8066, C_r:float=1.75, c_1:float=0.0328, c_2:float=4.575, 
                rho_Air:float=1.2256, C_D:float=0.28,
                motor_efficiency:float=0.91, driveline_efficiency:float=0.92, 
                braking_alpha:float=0.0411) -> None:
        """
        Properties of this class are intended to be immutable; 
        after initialization, modify them at your own risk.

        `vehicle`: The CARLA representation of the vehicle in question.

        `capacity`: Usable battery capacity in kWh.

        The remaining values are from https://doi.org/10.1016/j.apenergy.2016.01.097 .
        """
        self.vehicle = vehicle
        self.capacity = capacity
        physics_vehicle = vehicle.get_physics_control()
        self.mass = physics_vehicle.mass
        self.A_f = A_f
        self.gravity = gravity
        self.C_r = C_r
        self.c_1 = c_1
        self.c_2 = c_2
        self.rho_Air = rho_Air
        self.C_D = C_D
        self.motor_efficiency = motor_efficiency
        self.driveline_efficiency = driveline_efficiency
        self.motor_to_wheels_efficiency = motor_efficiency * driveline_efficiency
        self.braking_alpha = braking_alpha

        self.mg = self.mass * self.gravity
        self.term2_constants = self.mg * self.C_r / 1000
        self.term3_constants = self.rho_Air * self.A_f * self.C_D / 2
