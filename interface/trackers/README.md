# trackers
Vehicle physics tracking for CARLA simulator.


## Contents
- [charger.py](charger.py) is a class for wireless chargers.
- [consumption.md](consumption.md) contains notes from research.
- [energy_tracker.py](energy_tracker.py) tracks EV energy consumption.
    - Verification: Run [../tests/test_energy_tracker.py](../tests/test_energy_tracker.py).
- [ev.py](ev.py) contains a data class with info about a specific EV.
- [kinematics_tracker.py](kinematics_tracker.py) tracks vehicle location, speed, acceleration, road grade, and distance travelled.
- [soc_tracker.py](soc_tracker.py) adds state of charge and wireless charging functionalities to an `EnergyTracker`. 
- [time_tracker.py](time_tracker.py) tracks simulation time.
- [tracker.py](tracker.py) is a base class for `Tracker`s. 
