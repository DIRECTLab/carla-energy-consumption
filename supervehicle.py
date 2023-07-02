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
    def __init__(self, vehicle:Vehicle, agent_type:str) -> None:
        # https://arxiv.org/pdf/1908.08920.pdf%5D pg17
        drag = 0.23
        frontal_area = 2.22
        self.ev = EV(vehicle, capacity=50.0, A_f=frontal_area, C_D=drag)

        self.agent_type = agent_type
        self.agent = None
        if agent_type == 'traffic_manager':
            vehicle.set_autopilot(True)
        elif agent_type == 'cautious_behavior':
            self.agent = BehaviorAgent(vehicle, 'cautious')
        elif agent_type == 'normal_behavior':
            self.agent = BehaviorAgent(vehicle, 'normal')
        elif agent_type == 'aggressive_behavior':
            self.agent = BehaviorAgent(vehicle, 'aggressive')
        elif agent_type == 'basic':
            self.agent = BasicAgent(vehicle, target_speed=30)
        elif agent_type == 'constant':
            self.agent = ConstantVelocityAgent(vehicle, target_speed=30)

        self.trackers = list()

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
