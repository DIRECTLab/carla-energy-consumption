import warnings
import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning
import pygame

from control import Control


def brake_function(x, a, b, c):
    """
    Generic exponential function for brake input.
    """
    return a * np.exp(b * x) + c


if __name__ == '__main__':
    pygame.init()
    try:
        control = Control()
        cal_points = dict()
        input('Apply and release the brake, then press "Enter".')
        pygame.event.pump()
        brake = control.brake
        # brake = 1.
        print(brake)
        cal_points[0.] = brake
        input('Apply full brake and press "Enter".')
        pygame.event.pump()
        brake = control.brake
        # brake = -0.75
        print(brake)
        cal_points[1.] = brake
        input('Apply half brake and press "Enter".')
        pygame.event.pump()
        brake = control.brake
        # brake = 0.5
        print(brake)
        cal_points[0.5] = brake

        buffer = 0.15   # 15% of the brake range between 0 and half is not used
        cal_points[0.] = cal_points[0.] - (cal_points[0.] - cal_points[0.5]) * buffer

        if len(set(cal_points.values())) < len(cal_points):
            if cal_points[0.] == cal_points[1.]:
                print('Error: Full brake and released brake produced the same signal.')
            if cal_points[0.] == cal_points[0.5]:
                print('Error: Half brake and released brake produced the same signal.')
            if cal_points[0.5] == cal_points[1.]:
                print('Error: Full brake and half brake produced the same signal.')
            exit()

        guesses = (-0.2951958561021155, 1.4235477698527201, 1.1014918223893806)
        # Since the params should be a perfect fit, curve_fit might show this warning
        warnings.simplefilter('ignore', OptimizeWarning)
        (a, b, c), _ = curve_fit(brake_function, list(cal_points.values()), list(cal_points.keys()), p0=guesses)
        warnings.resetwarnings()

        print(f'{a=}')
        print(f'{b=}')
        print(f'{c=}')

    finally:
        pygame.quit()
