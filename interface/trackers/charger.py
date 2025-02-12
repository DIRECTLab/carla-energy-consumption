from carla import Location, DebugHelper, Color


class Charger:
    """
    Model for wireless charging.

    Receivers and transmitters are assumed to be double-D coils with the same dimensions. 
    Dimensions are those of the transmitter's coils. Maximum power transferred is `power * efficiency`, 
    which occurs when the receiver and the transmitter are perfectly aligned. 
    Power transfer decreases linearly to 0 in the direction of travel (treated as the y-axis) 
    and parabolically to 0 in the lane width direction (treated as the x-axis).

    See `notes` directory for papers about wireless power transfer justifying this model.
    """

    def __init__(self, front_left:Location, front_right:Location, back_right:Location, power:float, efficiency:float) -> None:
        """
        `front_left`: Location of the front left corner of this charger 
            as it appears when driving towards it and looking down from above. 
            "Front" means furthest from the vehicle as it is driving toward the charger 
            and closest to the vehicle after it passes the charger. 

        `front_right`: Location of the front right corner of this charger.

        `back_right`: Location of the back right corner of this charger.

        `power`: Maximum power used by charger in Watts.

        `efficiency`: Maximum charger-vehicle efficiency as a fraction assuming perfect alignment.
        """
        self.front_right = front_right
        self.front_left = front_left
        self.back_right = back_right
        self.power = power
        self.efficiency = efficiency
        self.max_power = efficiency * power
        self.length = front_right.distance(back_right)
        self.width = front_right.distance(front_left)
        self.center = (front_left + back_right) / 2
        self.i_hat = (front_right - front_left).make_unit_vector()
        self.j_hat = (back_right - front_right).make_unit_vector()
        self.k_hat = self.i_hat.cross(self.j_hat).make_unit_vector()
        self.events = list()
        # A somewhat arbitrary value that filters vehicles which obviously aren't charging
        self.max_range = 2 * (self.length + self.width)

    def transform_in(self, point:Location) -> Location:
        """
        Transforms `point` from global coordinates to this `Charger`'s coordinates.
        """
        # Get the vector from the charger's center to `point`
        point_translated = point - self.center
        # Get the magnitude of the projection of that vector onto the charger's axis vectors
        x = point_translated.dot(self.i_hat)
        y = point_translated.dot(self.j_hat)
        z = point_translated.dot(self.k_hat)
        return Location(x, y, z)

    def power_to_vehicle(self, point:Location) -> float:
        """
        Determine the power delivered to the vehicle in Watts, 
        assuming the center of the receiver is at `point`.
        """
        power = 0.0
        if self.center.distance(point) < self.max_range:    # Filter 99% of points
            transformed = self.transform_in(point)
            y_misalignment = abs(transformed.x)
            x_misalignment = abs(transformed.y)
            if y_misalignment < self.width and x_misalignment < self.length:
                x_scaling = 1 - x_misalignment / self.length
                y_scaling = 1 - (y_misalignment / self.width)**2
                scaling = x_scaling * y_scaling
                power = scaling * self.max_power
        return power

    def charge(self, point:Location, vehicle, time:float, dt:float):
        """
        Same as `power_to_vehicle`, but logs a charge event.
        """
        delivery = 0.0
        if self.center.distance(point) < self.max_range:    # Filter 99% of points
            delivery = self.power_to_vehicle(point)
            if delivery > 0:
                self.events.append({
                    'time': time,
                    'vehicle': vehicle,
                    'dt': dt,
                    'power_delivered': delivery,
                })
        return delivery

    def draw(self, debug:DebugHelper, life_time:float=0.0):
        """
        Draws the charging area.
        """
        center = Color(0,5,0)
        edges = Color(0,5,0)
        length = self.back_right - self.front_right
        back_left = self.front_left + length
        debug.draw_point(self.center, color=center, life_time=life_time)
        debug.draw_line(self.front_left, self.front_right, color=edges, life_time=life_time)
        debug.draw_line(self.front_right, self.back_right, color=edges, life_time=life_time)
        debug.draw_line(self.back_right, back_left,color=edges, life_time=life_time)
        debug.draw_line(back_left, self.front_left, color=edges, life_time=life_time)
