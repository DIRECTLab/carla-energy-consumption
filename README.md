# carla-energy-consumption
Energy consumption tracking for CARLA simulator.


## Contents
- [automatic_control.py](automatic_control.py) tracks a vehicle which is automatically controlled on the client side.

    Known issues:
    - Much like the average driver, the vehicle does not stop at stop signs.
    - Unlike the average driver, the vehicle brakes frequently instead of reducing throttle.

- `agents/` is copied over from `PythonAPI/carla/agents/`. See [its README](agents/README.md).

- `trackers/` contains code for tracking vehicle energy consumption as well as many other statistics. It also contains [example.py](trackers/example.py) demonstrating its usage. See [its README](trackers/README.md).
