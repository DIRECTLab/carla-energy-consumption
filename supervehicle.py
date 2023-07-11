import random
import networkx
from carla import Vehicle

from agents.navigation.behavior_agent import BehaviorAgent
from agents.navigation.basic_agent import BasicAgent
from agents.navigation.constant_velocity_agent import ConstantVelocityAgent

from trackers.ev import EV


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


class SuperVehicle:
    """
    Combines EV and Agent capabilities.
    """
    def __init__(self, vehicle:Vehicle, agent_type:str, ev_params:dict, init_hvac:float=0.0) -> None:
        """
        `agent_type`: One of 'traffic_manager', 'cautious_behavior', 'normal_behavior', 'aggressive_behavior', 'basic', 'constant'.

        `ev_params`: Parameters passed into the `EV` object. 
            `capacity` (usable battery capacity in kWh) must be specified; all others are optional.

        `init_hvac`: Initial power consumption due to HVAC in Watts.
        """
        self.ev = EV(vehicle, **ev_params)
        self.hvac = init_hvac

        self.__agent_type = None
        self.agent = None
        self.set_agent_type(agent_type)

        self.trackers = list()

    def get_agent_type(self):
        return self.__agent_type

    def set_agent_type(self, agent_type:str):
        """
        `agent_type`: One of 'traffic_manager', 'cautious_behavior', 'normal_behavior', 'aggressive_behavior', 'basic', 'constant'.
        """
        if agent_type == 'traffic_manager':
            self.ev.vehicle.set_autopilot(True)
            self.agent = None
        elif agent_type == 'cautious_behavior':
            self.agent = BehaviorAgent(self.ev.vehicle, 'cautious')
        elif agent_type == 'normal_behavior':
            self.agent = BehaviorAgent(self.ev.vehicle, 'normal')
        elif agent_type == 'aggressive_behavior':
            self.agent = BehaviorAgent(self.ev.vehicle, 'aggressive')
        elif agent_type == 'basic':
            self.agent = BasicAgent(self.ev.vehicle, target_speed=30)
        elif agent_type == 'constant':
            self.agent = ConstantVelocityAgent(self.ev.vehicle, target_speed=30)
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
        if self.agent is None:
            return
        if self.agent.done():
            self.choose_route(choices)

        control = self.agent.run_step()
        control.manual_gear_shift = False
        self.ev.vehicle.apply_control(control)

    def reset_vehicle(self, vehicle:Vehicle):
        """
        Sets all of its components to function with the new `vehicle` given.
        Does not change `EV` attributes (other than `vehicle`). 
        Its intended use is for respawning a vehicle identical to the original.
        """
        self.ev.vehicle = vehicle
        self.set_agent_type(self.__agent_type)  # This creates a new agent and/or sets autopilot
        for tracker in self.trackers:
            tracker.vehicle_id = vehicle.id
            tracker.start()
