# creation
Helper scripts for creating input files.

These scripts are intended to be run from the command line. Use the `-h` option for usage.


## Contents 

- [charger_options.py](charger_options.py) suggests parameters for wireless chargers in the current Map. It can provide many suggestions for the entire Map or a single suggestion near a specific point. The charging areas are displayed in the simulation, and parameters are printed to the screen. 
    - The command `python charger_options.py --number 10 --power 40000 --efficiency 0.95` will select 10 random locations on lanes within the current CARLA map and print the specifications of a charger CSV file for those transmitters. The power will be 40 kW, and the efficiency will be 95%. On UNIX systems, use `> chargers.csv` to save the output to a file for use in simulation.

- [charger_stuff.py](./charger_stuff.py) contains code shared between other files in this directory.

- [junction_chargers.py](./junction_chargers.py) gives parameters for wireless chargers near junctions.

- [junction_chargers_all.py](./junction_chargers_all.py) runs the same as junction_chargers.py but also creates a file called `all_junctions.csv` in the specified folder that combines the information for all the chargers at all the junctions.

- [optimal_chargers.py](./optimal_chargers.py) uses data from one or more prior simulations to determine the best places to install chargers for maximum utilization.
    - This script works best when data from multiple simulations is used. For example:
        ```
        # For this example, it is recommended to modify input/examples/tracked_agent.csv so that 100 agents are produced, so that there is 100 times as much data.
        python multitracking.py input/examples/tracked_agent.csv output/Town06_20min-1001/ -m Town06 --seed 1001 -t 1200 -d 0.05 -r
        python multitracking.py input/examples/tracked_agent.csv output/Town06_20min-1002/ -m Town06 --seed 1002 -t 1200 -d 0.05 -r
        python multitracking.py input/examples/tracked_agent.csv output/Town06_20min-1003/ -m Town06 --seed 1003 -t 1200 -d 0.05 -r
        python input/creation/optimal_chargers.py -m Town06 2.0 1.0 20 output/Town06_20min-1001/ output/Town06_20min-1002/ output/Town06_20min-1003/ --power 100_000 --efficiency 0.92 -i 0 > input/20chargers.csv
        ```
        This ensures that the chargers are not fine-tuned to a specific simulation run.

- [prepare_agents.py](./prepare_agents.py) is a script for creating an agent file such as [tracked_agent.csv](../examples/tracked_agent.csv).

- [propagate_chargers.py](./propagate_chargers.py) propagates chargers backwards through lanes.
