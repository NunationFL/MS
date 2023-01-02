import json

from agents.car import *
from agents.station import StationAgent
from agents.stop import StopAgent

funcs = [new_tesla_model_s,
         new_tesla_model_3,
         new_tesla_model_y,
         new_chevrolet_bolt,
         new_mustang_mach_e,
         new_renault_twizy,
         new_renault_zoe]

with open("../../files/step2.json", "r") as read_file:
    stop_points = json.load(read_file)

left = 1000
right = -1000
top = -1000
bottom = 1000

for idx in stop_points:
    point = stop_points[idx]
    if point[0] < bottom:
        bottom = point[0]
    if point[0] > top:
        top = point[0]
    if point[1] < left:
        left = point[1]
    if point[1] > right:
        right = point[1]
print((right - left), (top - bottom))


class Model(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, cars, stations, width, height):
        self.num_agents = cars + stations + len(stop_points)
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.cars_list = list()
        self.stations_list = list()
        self.stop_points = stop_points
        # Create agents
        self.setup_cars(cars)

        # for i in range(stations):
        self.setup_stations(cars)

        sum = 0
        for i in stop_points:
            a = StopAgent(cars + 3 + sum, self)
            x = int((stop_points[i][1] - left) * 100 * 2)
            y = int((stop_points[i][0] - bottom) * 100 * 2)
            self.grid.place_agent(a, (x, y))
            sum += 1

    def setup_stations(self, cars):
        a = StationAgent(cars, self, 2, 250)
        self.schedule.add(a)
        x, y = self.rand_point(left, bottom)
        self.grid.place_agent(a, (x, y))
        self.stations_list.append(a)

        a = StationAgent(1 + cars, self, 5, 44)
        self.schedule.add(a)
        x, y = self.rand_point(left, bottom)
        self.grid.place_agent(a, (x, y))
        self.stations_list.append(a)

        a = StationAgent(2 + cars, self, 1, 44)
        self.schedule.add(a)
        x, y = self.rand_point(left, bottom)
        self.grid.place_agent(a, (x, y))
        self.stations_list.append(a)

    def setup_cars(self, cars):
        for i in range(cars):
            a = self.random.choice(funcs)(i, self, self.random.randint(0, 100) / 100.0)
            idxs = self.random.sample(list(stop_points), 100)
            path = [stop_points[p] for p in idxs]
            a.set_path(path)
            self.schedule.add(a)
            self.cars_list.append(a)

            x, y = self.rand_point(left, bottom)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()

    def rand_point(self, left_point, bottom_point):
        p = self.random.choice(list(self.stop_points))
        p = self.stop_points[p]
        x = int((p[1] - left_point) * 100 * 2)
        y = int((p[0] - bottom_point) * 100 * 2)
        return x, y
