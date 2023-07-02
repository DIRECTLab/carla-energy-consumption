# input
Example input files for [example.py](../example.py).


- [chargers.csv](chargers.csv) is an example CSV file for loading wireless chargers. It demonstrates the following fields, required for all files of this type:
    - `x`: global x coordinate for center of charger (meters).
    - `y`: global y coordinate for center of charger (meters).
    - `z`: global z coordinate for center of charger (meters).
    - `width`: x-axis dimension for charging area (meters).
    - `length`: y-axis dimension for charging area (meters).
    - `height`: z-axis dimension for charging area (meters).
    - `roll`: rotation about the global x-axis (degrees).
    - `pitch`: rotation about the global y-axis (degrees).
    - `yaw`: rotation about the global z-axis (degrees).

- [directions.csv](directions.csv) is an example CSV file for loading predetermined directions. It demonstrates the `direction` field and accepted values.

    *In this mode, the vehicle will not perform lane changes. If lane changes are necessary, use a path file instead.*

- [path.csv](path.csv) is an example CSV file for loading a predetermined path. 
    This file demonstrates the following fields, required for all files of this type:
    - `x`: global x coordinate.
    - `y`: global y coordinate.
    - `z`: global z coordinate.

    *For proper functionality, ensure that points lie in roads and that there is at least one point for each road segment the vehicle should travel.* 

- [tracked_agents.csv](tracked_agents.csv) is an example CSV file for loading vehicles in [multitracking.py](multitracking.py). It demonstrates the following fields: 
    - `agent_type`: which agent to use for instructions. One of [traffic_manager, cautious_behavior, normal_behavior, aggressive_behavior, basic, constant].
    - `number`: number of vehicles with these specifications to spawn.

- [untracked_agents.csv](untracked_agents.csv) is a CSV for the `-u` option in [multitracking.py](multitracking.py). It follows the same pattern as [tracked_agents.csv](tracked_agents.csv). 
