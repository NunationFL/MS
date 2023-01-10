import mesa


class StationAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, spots, power, coords):
        super().__init__(unique_id, model)
        self.spots = spots  # battery in W.h
        self.power = power / 60
        self.using = list()
        self.waiting = list()
        self.coords = coords

    def start_charge(self, car):
        if len(self.using) < self.spots:
            self.using.append(car)
        else:
            self.waiting.append(car)

    def stop_charge(self, unique_id):
        self.using = [x for x in self.using if not x.unique_id == unique_id]
        if len(self.waiting) > 0:
            self.using.append(self.waiting.pop(0))

    def step(self):
        for car in self.using:
            car.charge(self.power)
            if car.battery_energy >= car.max_battery:
                car.stop_charge()

    @staticmethod
    def type():
        return "station"
