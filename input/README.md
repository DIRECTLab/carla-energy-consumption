# input
Example input files for [automatic_control.py](../automatic_control.py), [unitracking.py](../unitracking.py) and [multitracking.py](../multitracking.py).


## Contents
- [directions.csv](directions.csv) is an example CSV file for loading predetermined directions in [unitracking.py](../unitracking.py). It demonstrates the `direction` field and accepted values.

    *In this mode, the vehicle will not perform lane changes. If lane changes are necessary, use a path file instead.*

- [path.csv](path.csv) is an example CSV file for loading a predetermined path in [unitracking.py](../unitracking.py). 
    This file demonstrates the following fields, required for all files of this type:
    - `x`: global x coordinate.
    - `y`: global y coordinate.
    - `z`: global z coordinate.

    *For proper functionality, ensure that points lie in roads and that there is at least one point for each road segment the vehicle should travel.* 

- [prepare_agents.py](./prepare_agents.py) is a script for creating an agent file such as [tracked_agent.csv](./tracked_agent.csv).

- [Town06_intersection_chargers.csv](./Town06_intersection_chargers.csv) is an example CSV file for loading wireless chargers. 
    Receivers and transmitters are assumed to be double-D coils with the same dimensions, 
    which means that every entry in this file should have the same dimensions. 
    Dimensions and coordinates are those of the transmitter's coils. Maximum power transferred is `power * efficiency`, 
    which occurs when the receiver and the transmitter are perfectly aligned. 
    Power transfer decreases linearly to 0 in the direction of travel and parabolically to 0 in the lane width direction.

    See [notes](/notes/research.md) for papers about wireless power transfer justifying this model.

    The following fields are required for all files of this type:
    - `front_left`: Coordinates of the front left corner of this charger as it appears when driving towards it and looking down from above. "Front" means furthest from the vehicle as it is driving toward the charger and closest to the vehicle after it passes the charger. 
    - `front_right`: Coordinates of the front right corner of this charger.
    - `back_right`: Coordinates of the back right corner of this charger.
    - `power`: Power used by charger in Watts.
    - `efficiency`: Maximum charger-vehicle efficiency as a fraction assuming perfect alignment.

    To automatically generate a file of this type, see [charger_options.py](../navegation/charger_options.py).

- [tracked_agent.csv](tracked_agent.csv) is an example CSV file for loading vehicles in [multitracking.py](multitracking.py). It demonstrates the following required fields: 
    - `vehicle`: which vehicle blueprint to use. To view the available blueprints, run the CARLA example found at `PythonAPI\examples\vehicle_gallery.py`.
    - `agent_type`: which agent to use for instructions. One of [`traffic_manager`, `cautious_behavior`, `normal_behavior`, `aggressive_behavior`, `basic`, `constant`].

    In addition, the following fields are optional:
    - `number`: number of vehicles with these specifications to spawn.
        - Default: `1`.
    - `color`: RGB color of the vehicle.
    - `hvac`: power used for HVAC, in Watts.
        - Default: `0.0`.
    - `capacity`: usable battery capacity in kWh.
        - Default: `50.0`.
    - `init_soc`: initial state of charge of the vehicle as a fraction of full capacity.
        - Example: `init_soc = 0.80` with `capacity = 50.0` means that the battery currently has 40.0 (`0.80 * 50.0`) kWh of energy.
        - Default: `0.80`.
    - `lane_offset`: vehicle offset from center of lane, given in meters right of center. Applicable only to vehicles with `agent_type = traffic_manager`.
        - Default: `0.0`.

    These power consumption parameters are also optional, and descriptions can be found in [this article](https://doi.org/10.1016/j.apenergy.2016.01.097):
    - `A_f`
    - `gravity`
    - `C_r`
    - `c_1`
    - `c_2`
    - `rho_Air`
    - `C_D`
    - `motor_efficiency`
    - `driveline_efficiency`
    - `braking_alpha`

    For defaults, leave fields blank or do not include them.

- [tracked_agents.csv](./tracked_agents.csv) showcases all of the vehicles available in CARLA 0.9.14, for use in [multitracking.py](multitracking.py). It does not contain good EV parameters for all vehicles.

- [untracked_agents.csv](untracked_agents.csv) is a CSV for the `-u` option in [multitracking.py](multitracking.py). It follows the same pattern as [tracked_agent.csv](tracked_agent.csv). 
