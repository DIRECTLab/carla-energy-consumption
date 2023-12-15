Terminal 1:
1. Start the CARLA server

Terminal 2:
1. `python navigation/charger_options.py 2 1 -i 0 --power 100_000 --efficiency 0.95 --seed 0 -m Town06 > input/Town06chargers.csv`
1. `python multitracking.py input/tracked_agent.csv output/Town06_lap -w input/Town06chargers.csv --seed 0 -t 230 -d 0.05`

After Terminal 2 finishes, close the CARLA server. 
