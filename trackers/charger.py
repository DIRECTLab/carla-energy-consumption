import numpy as np
from carla import Location, DebugHelper


class Charger:
    """
    Wireless chargers
    """

    def __init__(self, front_left:Location, front_right:Location, back_right:Location, power:float, efficiency:float) -> None:
        """
        `front_left`: Location of the front left corner of the effective charging range of this charger 
            as it appears when driving towards it or looking down from above. 
            This point is part of the boundary of the effective charge range which is furthest from 
            the vehicle as it is driving toward the charger and closest to the vehicle after it passes the charger. 
            This boundary is represented as a rectangle. 

        `front_right`: Location of the front right corner of the effective charging range of this charger.

        `back_right`: Location of the back right corner of the effective charging range of this charger.

        `power`: Power used by charger in Watts.

        `efficiency`: Maximum charger-vehicle efficiency as a fraction assuming perfect alignment.
        """
        self.front_right = front_right
        self.front_left = front_left
        self.back_right = back_right
        self.length = front_right.distance(back_right)
        self.width = front_right.distance(front_left)
        self.center = (front_left + back_right) / 2
        self.transformation = self.__get_transformation(front_left, front_right, back_right)

        self.max_power = efficiency * power
        self.a = - self.max_power / (self.width/2)**2

    def __get_transformation(self, front_left:Location, front_right:Location, back_right:Location) -> np.ndarray:
        """
        Returns a matrix for transforming a point to the local coordinate system of this charger.
        This matrix should be multiplied on the left of the point.
        The input point should be represented as a vector of the form `[x,y,z,1]`,
        whereupon the resulting point will be a vector of the form `[x,y,z]`.
        """
        mid_right = (front_right + back_right) / 2
        X_ax = (mid_right - self.center).make_unit_vector()
        length = front_right - back_right
        mid_front = (front_right + front_left) / 2
        mid_back = mid_front - length
        Y_ax = (mid_back - self.center).make_unit_vector()
        Z_ax = X_ax.cross(Y_ax)
        rotation = np.array([
            [X_ax.x, X_ax.y, X_ax.z],
            [Y_ax.x, Y_ax.y, Y_ax.z],
            [Z_ax.x, Z_ax.y, Z_ax.z]
        ])
        translation = np.array([
            [1,0,0,-self.center.x],
            [0,1,0,-self.center.y],
            [0,0,1,-self.center.z],
        ])
        # Since we are multiplying on the left, this will translate the vector, then rotate it.
        transformation = np.matmul(rotation, translation)
        return transformation

    def transform_in(self, point:Location) -> Location:
        """
        Transforms `point` from global coordinates to this `Charger`'s coordinates.
        """
        point_np = np.array([point.x, point.y, point.z, 1])
        translated_np = np.matmul(self.transformation, point_np)
        translated = Location(translated_np[0], translated_np[1], translated_np[2])
        return translated

    def power_to_vehicle(self, point:Location) -> float:
        """
        Determine the power delivered to the vehicle in Watts, assuming the center of the vehicle is at `point`.
        """
        transformed = self.transform_in(point)
        y_misalignment = abs(transformed.x)
        x_misalignment = abs(transformed.y)
        if y_misalignment < self.width and x_misalignment <= self.length:
            power = self.a * y_misalignment**2 + self.max_power
        else:
            power = 0.0
        return power

    def draw(self, debug:DebugHelper, life_time:float=0.0):
        """
        Draws the charging area.
        """
        length = self.back_right - self.front_right
        back_left = self.front_left + length
        debug.draw_point(self.center, life_time=life_time)
        debug.draw_line(self.front_left, self.front_right, life_time=life_time)
        debug.draw_line(self.front_right, self.back_right, life_time=life_time)
        debug.draw_line(self.back_right, back_left, life_time=life_time)
        debug.draw_line(back_left, self.front_left, life_time=life_time)
