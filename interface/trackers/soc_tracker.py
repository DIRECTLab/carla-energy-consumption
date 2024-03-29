from carla import WorldSnapshot, Location

from .energy_tracker import EnergyTracker
from .ev import EV


class SocTracker(EnergyTracker):
    """
    Tracks EV battery charge.
    """

    def __init__(self, ev: EV, hvac: float = 0.0, init_soc: float = 1.0, wireless_chargers: list = []) -> None:
        """
        `hvac`: Power used for HVAC, in Watts.

        `init_soc`: Initial state of charge as a fraction.
        """
        super().__init__(ev, hvac)
        self.soc = init_soc
        self.soc_series = list()
        self.charge_power = list()
        self.wireless_chargers = wireless_chargers
        self.is_charging = False

    def _update(self, snapshot: WorldSnapshot, vehicle) -> None:
        # EnergyTracker functionality
        power = self.power(vehicle)
        self.power_consumed.append(power)
        energy_spent = self.energy_from_power(power, snapshot.delta_seconds)
        self.total_energy += energy_spent

        # Wireless charging
        location = vehicle.get_transform().location
        charging_energy = self.energy_from_chargers(location, snapshot.elapsed_seconds, snapshot.delta_seconds)
        self.is_charging = charging_energy > 0

        # Extra SocTracker functionality
        net_energy = charging_energy - energy_spent
        pct_gain = net_energy / self.ev.capacity
        self.soc = min(1.0, self.soc + pct_gain)
        self.soc_series.append(self.soc)

    def energy_from_chargers(self, location:Location, time:float, dt:float) -> float:
        power = 0
        for charger in self.wireless_chargers:
            power += charger.charge(location, self.vehicle_id, time, dt)
        self.charge_power.append(power)
        return self.energy_from_power(power, dt)
