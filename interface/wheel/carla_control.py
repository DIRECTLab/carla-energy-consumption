import math
import pygame
import carla

from .control import Control


class CarlaControl(Control):
    def __init__(self, world, start_in_autopilot):
        super().__init__()
        self._autopilot_enabled = start_in_autopilot
        world.player.set_autopilot(self._autopilot_enabled)
        self._reverse = False

    def _init_indices(self):
        parser = super()._init_indices()
        self._brake_a = float(parser.get('Brake', 'a'))
        self._brake_b = float(parser.get('Brake', 'b'))
        self._brake_c = float(parser.get('Brake', 'c'))

    @property
    def brake(self):
        """
        In order for this value to change, you must call a function from `pygame.event`.
        """
        brake = self._brake_a * math.e ** (self._brake_b * super().brake) + self._brake_c
        return max(0., min(1., brake))

    @property
    def throttle(self):
        """
        In order for this value to change, you must call a function from `pygame.event`.
        """
        # TODO: Simplify below
        throttle = 1.6 + (2.05 * math.log10(-0.7 * super().throttle + 1.4) - 1.2) / 0.92
        return max(0, min(1., throttle))

    def parse_events(self, world):
        control = carla.VehicleControl()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == self._restart_idx:
                    world.restart()
                elif event.button == self._info_idx:
                    world.hud.toggle_info()
                elif event.button == self._view_idx:
                    world.camera_manager.toggle_camera()
                elif event.button == self._weather_idx:
                    world.next_weather()
                elif event.button == self._reverse_idx:
                    control.gear = 1 if self._reverse else -1
                    self._reverse = not self._reverse
                elif event.button == self._sensor_idx:
                    world.camera_manager.next_sensor()
            elif event.type == pygame.JOYHATMOTION:
                if event.value == (0, 0):
                    world.camera_manager.look_forward()
                else:
                    degrees = math.degrees(math.atan2(*event.value))
                    world.camera_manager.set_yaw(degrees)

        if not self._autopilot_enabled:
            control.steer = self.steer
            control.brake = self.brake
            control.throttle = self.throttle
            control.hand_brake = bool(self._joystick.get_button(self._handbrake_idx))

            control.reverse = self._reverse
            world.player.apply_control(control)
