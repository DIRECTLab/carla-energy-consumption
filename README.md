# carla-energy-consumption

Energy consumption tracking for CARLA simulator.

All scripts in this directory run independently from each other and can be run from the command line. 
When in doubt, opt for [multitracking.py](multitracking.py). This program is the most up-to-date and offers most of the functionality of both [unitracking.py](unitracking.py) and [automatic_control.py](automatic_control.py), plus more.

More information about usage and options can be obtained with the `-h` option. 
See also [automated_quickstart.md](./docs/automated_quickstart.md).

## Contents

### [docs/](./docs/)

Contains additional software documentation.
* See [CARLA_DEMO.md](./docs/CARLA_DEMO.md) for instructions on how to get Carla running for demos.

### [automatic_control.py](automatic_control.py) 

Tracks a vehicle which is automatically controlled on the client side.

Basic Usage
1. Start the CARLA server.
2. Run `python automatic_control.py`.

Known issues:
- Much like the average driver, the vehicle does not stop at stop signs.
- Unlike the average driver, the vehicle brakes frequently instead of reducing throttle.

### [manual_control_steeringwheel.py](./manual_control_steeringwheel.py)

Tracks power usage of a vehicle which the user drives using a steering wheel controller.

Basic Usage
1. Start the CARLA server.
2. Run `python manual_control_steeringwheel.py input/examples/tracked_agent.csv`.

### [manual_control_reporting.py](manual_control_reporting.py) 

Does the same as manual_control_steeringwheel.py but with live reporting to the terminal.

Basic Usage
1. Start the CARLA server.
2. Run `python manual_control_reporting.py input/examples/tracked_agent.csv`.

### [multitracking.py](multitracking.py) 

* Tracks multiple vehicles at once. These vehicles can be controlled by the Traffic Manager or one of the agents under `agents/navigation/`.
* The `-d` option is strongly recommended. Try `0.05` at first. For BehaviorAgents, ensure `delta` time step is below `0.02`.

Basic Usage
1. Start the CARLA server.
2. Run `python multitracking.py input/examples/tracked_agent.csv output/`.
    - This will save all data to the `output/` directory, potentially overwriting data that is already there. `output/` can be replaced by any path to a directory or potential directory.

### [unitracking.py](unitracking.py) 

* Shows a usage example allowing greater control over a single vehicle. This spawns traffic and tracks energy usage and other data about a simulated Tesla Model 3, displaying updates every second. At the end, it graphs the power consumed as compared with velocity, acceleration and road grade, then plots a heatmap of the areas the vehicle travelled to. 
* The `-t` option is strongly recommended.

Basic Usage
1. Start the CARLA server.
2. Run `python unitracking.py`.


### [interface/](./interface/) 

* This is an interface between the user-facing programs contained in this directory and the inner workings of the core logic.
* See [its README](./interface/README.md).

### [input/](./input/) 

* Contains example input files for [automatic_control.py](automatic_control.py), [unitracking.py](unitracking.py) and [multitracking.py](multitracking.py). It also contains some scripts to help create those files. 
* See [its README](input/examples/README.md) for input file documentation.

### [navigation/](./navigation/) 

* Contains some functions for getting oriented to CARLA maps and wireless chargers.
* See [its README](navigation/README.md). 

### [plots/](./plots/) 

* Contains code for example plots based on simulation data.

### [tests/](./tests/) 

* Has all of the unit tests for the project.
* See [its README](tests/README.md).

## Requirements

Follow CARLA [installation instructions](https://carla.readthedocs.io/en/0.9.14/start_quickstart/) for both server and client. In addition, use `pip` or `conda` to install `matplotlib`, `pandas`, `shapely`, and `networkx`. This code was tested on CARLA `v0.9.14`, Python `v3.8.16`.

## License

All software is included under the [MIT License](https://opensource.org/license/mit/).
