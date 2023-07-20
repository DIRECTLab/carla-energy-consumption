from carla import Transform, Vector3D, BoundingBox, Location


class Charger:
    """
    Wireless chargers
    """

    def __init__(self, transform:Transform, length:float, width:float, power:float, efficiency:float) -> None:
        """
        `transform`: Location and rotation of charging area.

        `length`: Length of the charging pad in meters.

        `width`: Effective charging area width in meters.

        `power`: Power used by charger in Watts.

        `efficiency`: Maximum charger-vehicle efficiency as a fraction assuming perfect alignment.
        """
        extent = Vector3D(length / 2, width / 2, 2)     # z-axis is hard-coded at +/- 2 m.
        self.bbox = BoundingBox(Location(), extent)
        self.transform = transform
        self.effective_power = efficiency * power

    def power_to_vehicle(self, point:Location) -> float:
        """
        Determine the power delivered to the vehicle in Watts, assuming the center of the vehicle is at `point`.
        """
        if self.bbox.contains(point, self.transform):
            return self.effective_power
        else:
            return 0.0
