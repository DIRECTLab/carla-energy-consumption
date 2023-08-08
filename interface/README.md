# interface
Modules for use by the main programs.


## Contents

- [hud.py](./hud.py) controls the display for [manual_control_steeringwheel.py](../manual_control_steeringwheel.py).

- [loading.py](loading.py) is a module for loading input files.

- [reporting.py](reporting.py) is a module for reporting tracking data.

- [supervehicle.py](supervehicle.py) combines `EV`, `Agent`, and `Tracker` functionality.

- [world.py](./world.py) controls the player and scene for [manual_control_steeringwheel.py](../manual_control_steeringwheel.py).

- [agents/](agents/README.md) is copied over from `PythonAPI/carla/agents/`. 

- [trackers/](trackers/README.md) contains code for tracking vehicle energy consumption as well as many other statistics. 

- [wheel/](./wheel/README.md) contains code for calibrating and interpreting a steering wheel controller. 
