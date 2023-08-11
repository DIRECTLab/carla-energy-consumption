import numpy as np
from carla import Location, DebugHelper, Color


class Charger:
    """
    Model for wireless charging.

    Chargers are assumed to have an effective charge range which is represented as a rectangle. 
    Alignment with the center line of the charger running from back to front results in the highest power transfer 
    (given by `power * efficiency`), while power transfer decreases parabolically to `0` at the far left and right 
    of the effective charge range.

    For real-life results reflecting this implementation, see https://doi.org/10.3390/en10030315 - especially Figure 5.
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
        self.half_length = front_right.distance(back_right) / 2
        self.half_width = front_right.distance(front_left) / 2
        self.center = (front_left + back_right) / 2
        self.transformation = self.__get_transformation(front_left, front_right, back_right)

        # Power delivery follows the equation a*x^2+b, where a is a negative constant, 
        # x is misalignment from the charger's y-axis and b is the maximum power
        self.max_power = efficiency * power
        self.a = - self.max_power / self.half_width**2

        self.events = list()

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
        # Since we are multiplying on the left of the vector, this will translate the vector, then rotate it.
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

        Power delivery follows the equation `a*x^2+b`, where `a` is a negative constant, 
        `x` is misalignment from the charger's y-axis and `b` is the maximum power.
        """
        transformed = self.transform_in(point)
        y_misalignment = abs(transformed.x)
        x_misalignment = abs(transformed.y)
        if y_misalignment < self.half_width and x_misalignment <= self.half_length:
            power = max(self.a * y_misalignment**2 + self.max_power, 0.0)
        else:
            power = 0.0
        return power
    
    def charge(self, point:Location, dt:float):
        """
        Same as `power_to_vehicle`, but updates the charger's energy consumption.
        """
        delivery = self.power_to_vehicle(point)
        if delivery > 0:
            self.events.append({
                'loc': f"{point.x}, {point.y}, {point.z}",
                'dt': dt,
                'power_delivered': delivery,
            })
        return delivery

    def draw(self, debug:DebugHelper, life_time:float=0.0):
        """
        Draws the charging area.
        """
        center = Color(255,0,1)
        edges = Color(30,255,0)
        length = self.back_right - self.front_right
        back_left = self.front_left + length
        debug.draw_point(self.center, color=center, life_time=life_time)
        debug.draw_line(self.front_left, self.front_right, color=edges, life_time=life_time)
        debug.draw_line(self.front_right, self.back_right, color=edges, life_time=life_time)
        debug.draw_line(self.back_right, back_left,color=edges, life_time=life_time)
        debug.draw_line(back_left, self.front_left, color=edges, life_time=life_time)
