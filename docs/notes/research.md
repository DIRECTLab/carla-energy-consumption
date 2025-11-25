# Research notes

- [This article](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9657075/) uses SUMO and CARLA to train intersection crossing.

- [This site](https://www.nrel.gov/transportation/wireless-electric-vehicle-charging.html) is a treasure trove of WPT links.

- [A great article about the current and future state of wireless power transfer](https://tec.ieee.org/newsletter/march-2018/wireless-charging-for-electric-vehicles)
  - Charging efficiency >90%
  - Advantages and disadvantages of dynamic electric vehicle charging

- *Dynamic Wireless Power Transfer (DWPT)*: WPT while vehicle is moving
- *Quasi-Dynamic Wireless Power Transfer*: WPT while vehicle is temporarily stationary, e.g. traffic lights
- *Static Wireless Power Transfer*: WPT while vehicle is parked

- [Fixed-route DWPT case study](https://www.sciencedirect.com/science/article/pii/S0306261920315476?via%3Dihub)
  - Confirms parabolic nature with respect to lane alignment
  - Trapezoidal with respect to travel direction
  - 100 kW, 5 m chargers

- [Optimal wireless charger for both heavy- and light-duty vehicles](https://ieeexplore.ieee.org/abstract/document/8450095)
  - 3 kW auxillary power for LDV, 6 kW for HDV
  - Trapezoidal approximation of efficiency in direction of travel
  - Make the receiver as big as possible, the transmitter at least as big as the receiver
    - Length of LDV: 4.45m
    - Available width within axle track of LDV: 1 m
  - Analyzes coverage needed for stable charge at 70 mph

- ["A Review of High-Power Wireless Power Transfer"](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=7993277)
  - Comparison table of several WPT systems, including power and efficiency
  - Max of 50 kW
  - Coil efficiency of 90-97%

- [Double-D coil models](https://ieeexplore.ieee.org/document/7802607)
  - Notes that voltage due to the vehicle moving relative to the transmitter is ignored - we should do the same
  - Trapezoidal in direction of travel, with equations for different sizes
    - See Equation 8, supported by Figure 12 and Figure 1

- [Wireless charging with experimental results](https://doi.org/10.3390/en10030315)
  - Angular misalignment doesn't matter
  - Lateral misalignment is parabolic
