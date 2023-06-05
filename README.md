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
```python example.py -s 0 0 0 -n 1 -t 0```

100 simulation seconds in 100 real seconds.

```python example.py -s 0 0 0 -n 1 -t 0.025```

222 simulation seconds in 100 real seconds

```python example.py -s 0 0 0 -n 1 -t 0.025 --asynch```

217 simulation seconds in 100 real seconds

```python example.py -s 0 0 0 -n 1 -t 0.01```

86 simulation seconds in 100 real seconds

```python example.py -s 0 0 0 -n 1 -t 0.05```

440 simulation seconds in 100 real seconds

```python example.py -s 0 0 0 -n 100 -t 0.025```

124 simulation seconds in 100 real seconds

### Low Mode Rendering
```python example.py -s 0 0 0 -n 1 -t 0.025```

345 simulation seconds in 100 real seconds

### Off-Screen Rendering
```python example.py -s 0 0 0 -n 1 -t 0.025```

234 simulation seconds in 100 real seconds

### No Rendering
```python example.py -s 0 0 0 -n 1 -t 0.01 -r n```

851 simulation seconds in 100 real seconds

```python example.py -s 0 0 0 -n 1 -t 0.025 -r n```

2054 simulation seconds in 100 real seconds

```python example.py -s 0 0 0 -n 1 -t 0.05 -r n```

4002 simulation seconds in 100 real seconds
