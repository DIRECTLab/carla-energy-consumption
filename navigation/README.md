# navigation
Help with understanding CARLA's coordinate system and wireless charger placement within that system.

These scripts are intended to be run from the command line. Use the `-h` option for usage.


## Contents

- [charger_options.py](charger_options.py) suggests parameters for wireless chargers in the current Map. It can provide many suggestions for the entire Map or a single suggestion near a specific point. The charging areas are displayed in the simulation, and parameters are printed to the screen. 
    - The command `python charger_options.py --number 10 --power 40000 --efficiency 0.95` will select 10 random locations on lanes within the current CARLA map and print the specifications of a charger CSV file for those transmitters. The power will be 40 kW, and the efficiency will be 95%. On UNIX systems, use `> chargers.csv` to save the output to a file for use in simulation.

- [charger_stuff.py](./charger_stuff.py) contains code shared between other files in this directory.

- [coordinates.py](coordinates.py) highlights the x- and y-axes at (0,0). Each square drawn is 1m x 1m.

- [draw_chargers.py](draw_chargers.py) highlights the wireless chargers specified. Navigate beneath the ground to view wireless chargers placed there, or place them at ground level as recommended.

- [junction_chargers.py](./junction_chargers.py) gives parameters for wireless chargers near junctions.

- [lane_distance.py](./lane_distance.py) reports the distance covered by the lanes in a specific map. See also `road_area.py`.

- [optimal_chargers.py](./optimal_chargers.py) uses data from one or more prior simulations to determine the best places to install chargers for maximum utilization.
    - This script works best when data from multiple simulations is used. For example:
        ```
        python multitracking.py input/tracked_agent.csv output/Town06_20min-1001/ -m Town06 --seed 1001 -t 1200 -d 0.05 -r
        python multitracking.py input/tracked_agent.csv output/Town06_20min-1002/ -m Town06 --seed 1002 -t 1200 -d 0.05 -r
        python multitracking.py input/tracked_agent.csv output/Town06_20min-1003/ -m Town06 --seed 1003 -t 1200 -d 0.05 -r
        python navigation/optimal_chargers.py -m Town06 2.0 1.0 20 output/Town06_20min-1001/ output/Town06_20min-1002/ output/Town06_20min-1003/ --power 100_000 --efficiency 0.92 -i 0 > input/20chargers.csv
        ```
        This ensures that the chargers are not fine-tuned to a specific simulation run.

- [propagate_chargers.py](./propagate_chargers.py) propagates chargers backwards through lanes.

- [road_area.py](./road_area.py) approximates the  driveable road area within the current Map.


## Additional Notes

- CARLA's coordinate system has the z-axis up with the y-axis clockwise of the x-axis when looking down from above. This is a left-handed system.

- Each unit along the coordinate system is a meter.

- A CARLA `Rotation` object is extremely unintuitive. See [its entry](https://carla.readthedocs.io/en/0.9.14/python_api/#carla.Rotation) in the API documentation. There are two things that make this object difficult to understand:

    - As shown (but not emphasized) in the documentation, `roll` and `pitch` rotate counterclockwise while `yaw` rotates clockwise.
    - Despite the declaration order being `pitch, yaw, roll`, my experiments show that rotations are applied in the order `roll`, `pitch`, then `yaw`. 

    Due to the difficulty I had in understanding this system (and anticipating that other users would have similar difficulty), I am refraining from relying heavily upon CARLA `Rotation` objects and the `Transform` objects which contain them.
