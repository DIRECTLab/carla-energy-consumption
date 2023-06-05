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

## Simulation Options
For an idea of how fast the simulation will run:

### Epic Mode Rendering
```python example.py -n 1 -s 0 0 0```

101 simulation seconds in 101 real seconds.

```python example.py -n 1 -s 0 0 0 -t 0.025```

246 simulation seconds in 101 real seconds

```python example.py -n 100 -s 0 0 0 -t 0.025```

141 simulation seconds in 101 real seconds

### Low Mode Rendering
```python example.py -n 1 -s 0 0 0```

101 simulation seconds in 101 real seconds.

```python example.py -n 1 -s 0 0 0 -t 0.05```

403 simulation seconds in 101 real seconds

```python example.py -n 1 -s 0 0 0 -t 0.1```

877 simulation seconds in 101 real seconds

```python example.py -n 100 -s 0 0 0 -t 0.05```

244 simulation seconds in 101 real seconds

### No Rendering
```python example.py -n 1 -s 0 0 0 -t 0.05 -r n```

4013 simulation seconds in 101 real seconds

```python example.py -n 100 -s 0 0 0 -t 0.05 -r n```

349 simulation seconds in 101 real seconds
