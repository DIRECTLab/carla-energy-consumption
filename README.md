# carla-energy-consumption
Energy consumption tracking for CARLA simulator.


## Contents
- `consumption.md` contains notes from research.
- `distance_tracker.py` tracks vehicle distance travelled.
- `energy_tracker.py` tracks EV energy consumption.
- `example.py` shows a usage example.

## Requirements
Follow CARLA installation instructions for both server and client. This code was tested on CARLA `v0.9.14`, Python `v3.8.16`.

## Results
Tesla Model 3 with traffic, Town10:
118476 m on 13.4884 kWh (18.3222 kWh / 100 mi)

Tesla Model 3 with traffic, Town04:
134928 m on 17.3534 kWh (20.6981 kWh / 100 mi)
