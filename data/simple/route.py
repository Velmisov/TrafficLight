import random
import pandas as pd
import numpy as np

from data.simple import info


class Route:

    def __init__(self, number_of_vehicles):
        self.vehicles_to_create = number_of_vehicles
        self.file_name = info.PATH+".rou.xml"

        xls = pd.ExcelFile("data\simple\coefficients.xlsx")
        self.data = xls.parse("Coefficients")
        xls.close()
        self.data.columns = ["id\\routes"]+info.ROUTES
        self.coefficients = [0] * len(info.ROUTES)

        # random.seed(7)

    def __new_vehicle(self, veh_id, veh_type, route_id, depart):
        return '<vehicle id="%d" type="%s" route="%s" depart="%d" />' % \
               (veh_id, veh_type, route_id, depart)

    def set_coefficients(self, coefficients):
        self.coefficients = coefficients

    def __next_coefficients(self):
        coefficients_id = random.randint(0, 14)
        for i in range(len(info.ROUTES)):
            self.coefficients[i] = self.data[info.ROUTES[i]][coefficients_id]

    def next(self):
        if np.sum(self.coefficients) == 0:
            self.__next_coefficients()
        with open(self.file_name, "w") as routes_file:
            print('''<routes>
            <vType id="type1" accel="0.8" decel="4.5" sigma="0.5" length="5" maxSpeed="70" />
            <vType id="type2" accel="0.8" decel="4.5" sigma="0.5" length="5" maxSpeed="70" color="1,1,1" />
            <route id="route1to2" edges="1totl tlto2" />
            <route id="route1to4" edges="1totl tlto4" />
            <route id="route2to1" edges="2totl tlto1" />
            <route id="route2to3" edges="2totl tlto3" />
            <route id="route3to4" edges="3totl tlto4" />
            <route id="route3to1" edges="3totl tlto1" />
            <route id="route4to3" edges="4totl tlto3" />
            <route id="route4to2" edges="4totl tlto2" />''', file=routes_file)

            vehicle_id = 0
            for i in range(self.vehicles_to_create):
                for route_id in range(len(self.coefficients)):
                    if random.random() < self.coefficients[route_id]:
                        print(self.__new_vehicle(vehicle_id, "type2", info.ROUTES[route_id], i), file=routes_file)
                        vehicle_id += 1

            print("</routes>", file=routes_file)
        self.coefficients = [0] * len(info.ROUTES)
