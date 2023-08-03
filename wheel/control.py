from configparser import ConfigParser
import pygame


class Control:
    def __init__(self) -> None:
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        if joystick_count < 1:
            raise ValueError("Please Connect a Wheel")
        if joystick_count > 1:
            raise ValueError("Please Connect Just One Wheel")

        self._joystick = pygame.joystick.Joystick(0)
        self._joystick.init()

        self._parser = ConfigParser()
        self._parser.read('wheel_config.ini')
        self._steer_idx = int(
            self._parser.get('G29 Racing Wheel', 'steering_wheel'))
        self._throttle_idx = int(
            self._parser.get('G29 Racing Wheel', 'throttle'))
        self._brake_idx = int(self._parser.get('G29 Racing Wheel', 'brake'))
        self._reverse_idx = int(self._parser.get('G29 Racing Wheel', 'reverse'))
        self._handbrake_idx = int(
            self._parser.get('G29 Racing Wheel', 'handbrake'))
        
        # self.numaxes = self._joystick.get_numaxes
        
    def brake(self):
        pygame.event.get()
        return self._joystick.get_axis(self._brake_idx)
