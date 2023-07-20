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
        self.max_power = efficiency * power
        self.a = - self.max_power / (width/2)**2

    def get_lateral_misalignment(self, point:Location) -> float:
        """
        Return the lateral misalignment of `point` from this charger.
        """

    def power_to_vehicle(self, point:Location) -> float:
        """
        Determine the power delivered to the vehicle in Watts, assuming the center of the vehicle is at `point`.
        """
        if self.bbox.contains(point, self.transform):
            lat_misalignment = self.get_lateral_misalignment()
            return self.a * lat_misalignment**2 + self.max_power
        else:
            return 0.0
