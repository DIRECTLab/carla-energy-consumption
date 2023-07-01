from trackers.ev import EV


class SuperVehicle:
    def __init__(self, ev:EV) -> None:
        self.ev = ev
        self.trackers = list()
