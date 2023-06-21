from carla import WorldSnapshot
from energy_tracker import EnergyTracker

from ev import EV


class SocTracker(EnergyTracker):
    """
    Tracks EV battery charge.
    """

    def __init__(self, ev: EV, hvac: float = 0.0, init_soc: float = 1.0) -> None:
        """
        `hvac`: Power used for HVAC, in Watts.

        `init_soc`: Initial state of charge as a fraction.
        """
        super().__init__(ev, hvac)
        self.soc = init_soc
        self.soc_series = [init_soc]

    def _update(self, snapshot: WorldSnapshot, vehicle) -> None:
        # EnergyTracker functionality
        power = self.power(vehicle)
        self.power_series.append(power)
        energy = self.energy_from_power(power, snapshot.delta_seconds)
        self.total_energy += energy

        # Extra SocTracker functionality
        self.soc -= energy / self.ev.capacity
        self.soc_series.append(self.soc)
