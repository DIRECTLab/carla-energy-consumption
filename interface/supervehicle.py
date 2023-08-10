import random
import networkx
from carla import Vehicle, VehicleControl, Vector3D

from .agents.behavior_agent import BehaviorAgent
from .agents.basic_agent import BasicAgent
from .agents.constant_velocity_agent import ConstantVelocityAgent

from .trackers.ev import EV
from .trackers.time_tracker import TimeTracker
from .trackers.soc_tracker import SocTracker
from .trackers.kinematics_tracker import KinematicsTracker


def choose_route(agent, choices, tries=5) -> bool:
    """
    return: Whether a route was chosen.
    """
    while tries:
        destination = random.choice(choices).location
        try:
            agent.set_destination(destination)
            return True
        except networkx.exception.NetworkXNoPath:
            print(f'Failed to find a route to {destination}')
            tries -= 1
    return False


class SuperVehicle(EV):
    """
    Combines EV and Agent capabilities.
    """
    def __init__(self, vehicle:Vehicle, agent_type:str, ev_params:dict, init_soc:float, init_hvac:float=0.0) -> None:
        """
        `agent_type`: One of 'traffic_manager', 'cautious_behavior', 'normal_behavior', 'aggressive_behavior', 'basic', 'constant'.

        `ev_params`: Parameters passed into the `EV` object. 
            `capacity` (usable battery capacity in kWh) must be specified; all others are optional.

        `init_soc`: Initial state of charge of the vehicle as a fraction of full capacity.

        `init_hvac`: Initial power consumption due to HVAC in Watts.
        """
        super().__init__(vehicle, **ev_params)
        self.init_soc = init_soc
        self.hvac = init_hvac
        self.trackers = dict()
        self.running = False

        self.__agent_type = None
        self.agent = None
        self.set_agent_type(agent_type)

    def get_agent_type(self):
        return self.__agent_type

    def set_agent_type(self, agent_type:str):
        """
        Creates a new agent and/or sets autopilot.

        `agent_type`: One of 'traffic_manager', 'cautious_behavior', 'normal_behavior', 'aggressive_behavior', 'basic', 'constant'.
        """
        if agent_type == 'traffic_manager':
            self.vehicle.set_autopilot(True)
            self.agent = None
        elif agent_type == 'cautious_behavior':
            self.agent = BehaviorAgent(self.vehicle, 'cautious')
        elif agent_type == 'normal_behavior':
            self.agent = BehaviorAgent(self.vehicle, 'normal')
        elif agent_type == 'aggressive_behavior':
            self.agent = BehaviorAgent(self.vehicle, 'aggressive')
        elif agent_type == 'basic':
            self.agent = BasicAgent(self.vehicle, target_speed=30)
        elif agent_type == 'constant':
            self.agent = ConstantVelocityAgent(self.vehicle, target_speed=30)
        self.running = True
        self.__agent_type = agent_type

    def choose_route(self, choices, tries=5) -> bool:
        """
        Has no effect unless an agent has been set.

        return: Whether a route was chosen.
        """
        if self.agent is None:
            return False
        return choose_route(self.agent, choices, tries)

    def run_step(self, choices):
        if self.running:
            soc_tracker = self.trackers.get('soc')
            has_charge = soc_tracker == None or soc_tracker.soc > 0.0
            if has_charge:
                if self.agent is not None:
                    if self.agent.done():
                        self.choose_route(choices)

                    control = self.agent.run_step()
                    control.manual_gear_shift = False
                    self.vehicle.apply_control(control)
            else:
                if self.agent is None:
                    self.vehicle.set_autopilot(False)
                self.vehicle.apply_control(VehicleControl(gear=1))
                self.running = False

    def reset_vehicle(self, vehicle:Vehicle):
        """
        Sets all of its components to function with the new `vehicle` given.
        Does not change `EV` attributes (other than `vehicle`). 
        Its intended use is for respawning a vehicle identical to the original.
        """
        self.vehicle = vehicle
        self.set_agent_type(self.__agent_type)
        for tracker in self.trackers.values():
            tracker.vehicle_id = vehicle.id

    def initialize_trackers(self, wireless_chargers):
        """
        `wireless_chargers`: Chargers to pass to `SocTracker`.
        """
        self.stop_tracking()
        self.trackers['time'] = TimeTracker(self.vehicle)
        self.trackers['kinematics'] = KinematicsTracker(self.vehicle)
        soc_tracker = self.trackers.get('soc')
        if soc_tracker is None:
            self.trackers['soc'] = SocTracker(self, self.hvac, self.init_soc, wireless_chargers)
        else:
            self.trackers['soc'] = SocTracker(self, self.hvac, soc_tracker.soc, wireless_chargers)
        for tracker in self.trackers.values():
            tracker.start()

    def stop_tracking(self):
        for tracker in self.trackers.values():
            tracker.stop()
