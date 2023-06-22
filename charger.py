from carla import Transform, Vector3D, BoundingBox, Location


class Charger:
    """
    Wireless chargers
    """

    def __init__(self, transform:Transform, extent:Vector3D) -> None:
        """
        `transform`: Location and rotation of charging area.

        `extent`: Vector from the center of the charging area to a vertex.
        """
        self.bbox = BoundingBox(Location(), extent)
        self.transform = transform
    
    def power_to_vehicle(self, point:Location) -> float:
        """
        Determine the power delivered to the vehicle in Watts, assuming the center of the vehicle is at `point`.
        With the right expertise, this method could be improved.
        """
        if self.bbox.contains(point, self.transform):
            return 100_000.0   # I have no idea what to put here . . .
        else:
            return 0.0
