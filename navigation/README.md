# navigation
Help with understanding CARLA's coordinate system and wireless charger placement within that system.

These scripts are intended to be run from the command line. Use the `-h` option for usage.


## Contents

- [coordinates.py](coordinates.py) highlights the x- and y-axes at (0,0). Each square drawn is 1m x 1m.

- [draw_chargers.py](draw_chargers.py) highlights the wireless chargers specified. Navigate beneath the ground to view wireless chargers placed there, or place them at ground level as recommended.

- [lane_distance.py](./lane_distance.py) reports the distance covered by the lanes in a specific map. See also `road_area.py`.

- [road_area.py](./road_area.py) approximates the  driveable road area within the current Map.


## Additional Notes

- CARLA's coordinate system has the z-axis up with the y-axis clockwise of the x-axis when looking down from above. This is a left-handed system.

- Each unit along the coordinate system is a meter.

- A CARLA `Rotation` object is extremely unintuitive. See [its entry](https://carla.readthedocs.io/en/0.9.14/python_api/#carla.Rotation) in the API documentation. There are two things that make this object difficult to understand:

    - As shown (but not emphasized) in the documentation, `roll` and `pitch` rotate counterclockwise while `yaw` rotates clockwise.
    - Despite the declaration order being `pitch, yaw, roll`, my experiments show that rotations are applied in the order `roll`, `pitch`, then `yaw`. 

    Due to the difficulty I had in understanding this system (and anticipating that other users would have similar difficulty), I am refraining from relying heavily upon CARLA `Rotation` objects and the `Transform` objects which contain them.
