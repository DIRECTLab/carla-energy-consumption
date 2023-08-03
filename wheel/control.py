import os
from configparser import ConfigParser
import pygame


class Control:
    def __init__(self) -> None:
        self._init_wheel()
        self._init_presets()

    def _init_wheel(self):
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        if joystick_count < 1:
            raise ValueError("Please Connect a Wheel")
        if joystick_count > 1:
            raise ValueError("Please Connect Just One Wheel")

        self._joystick = pygame.joystick.Joystick(0)
        self._joystick.init()

    def _init_presets(self):
        self._parser = ConfigParser()
        self._parser.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wheel_config.ini'))
        self._steer_idx = int(self._parser.get('G29 Racing Wheel', 'steering_wheel'))
        self._throttle_idx = int(self._parser.get('G29 Racing Wheel', 'throttle'))
        self._brake_idx = int(self._parser.get('G29 Racing Wheel', 'brake'))
        self._reverse_idx = int(self._parser.get('G29 Racing Wheel', 'reverse'))
        self._handbrake_idx = int(self._parser.get('G29 Racing Wheel', 'handbrake'))

    @property
    def steer(self):
        """
        In order for this value to change, you must call a function from `pygame.event`.
        """
        return self._joystick.get_axis(self._steer_idx)

    @property
    def brake(self):
        """
        In order for this value to change, you must call a function from `pygame.event`.
        """
        return self._joystick.get_axis(self._brake_idx)

    @property
    def throttle(self):
        """
        In order for this value to change, you must call a function from `pygame.event`.
        """
        return self._joystick.get_axis(self._throttle_idx)
