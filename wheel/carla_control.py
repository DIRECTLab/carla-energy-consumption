import math
import pygame
import carla

from control import Control


class CarlaControl(Control):
    def __init__(self, world, start_in_autopilot):
        super().__init__()
        self._autopilot_enabled = start_in_autopilot
        self._controller = carla.VehicleControl()
        world.player.set_autopilot(self._autopilot_enabled)

    @property
    def brake(self):
        """
        In order for this value to change, you must call a function from `pygame.event`.
        """
        brake = -0.2951958561021155 * math.e ** (1.4235477698527201 * super().brake) + 1.1014918223893806
        return max(0., min(1., brake))

    @property
    def throttle(self):
        """
        In order for this value to change, you must call a function from `pygame.event`.
        """
        # TODO: Simplify below
        throttle = 1.6 + (2.05 * math.log10(-0.7 * super().throttle + 1.4) - 1.2) / 0.92
        return max(0., min(1., throttle))

    def parse_events(self, world, clock):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    world.restart()
                elif event.button == 1:
                    world.hud.toggle_info()
                elif event.button == 2:
                    world.camera_manager.toggle_camera()
                elif event.button == 3:
                    world.next_weather()
                elif event.button == self._reverse_idx:
                    self._controller.gear = 1 if self._controller.reverse else -1
                elif event.button == 23:
                    world.camera_manager.next_sensor()

        if not self._autopilot_enabled:
            self._parse_vehicle_wheel()
            self._controller.reverse = self._controller.gear < 0
            world.player.apply_control(self._controller)

    def _parse_vehicle_wheel(self):
        self._controller.steer = self.steer
        self._controller.brake = self.brake
        self._controller.throttle = self.throttle
        self._controller.hand_brake = bool(self._joystick.get_button(self._handbrake_idx))
