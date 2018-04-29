import random
import pandas as pd


class Route:

    def __init__(self, number):
        self.number = number
        self.file_name = "data\simple\simple.rou.xml"
        self.types = ["type1", "type2"]
        self.routes = ["route1to2", "route1to4", "route2to1", "route2to3", "route3to4", "route3to1", "route4to3",
                       "route4to2"]

        xls = pd.ExcelFile("data\simple\coefficients.xlsx")
        self.data = xls.parse("Coefficients")
        xls.close()
        self.data.columns = ["id\\routes"]+self.routes
        self.last_coefficients_id = 0
        self.coefficients = [0 for i in range(len(self.routes))]

        random.seed(7)

    def __new_vehicle(self, id, type, route_id, depart):
        return '<vehicle id="%d" type="%s" route="%s" depart="%d" />' % \
               (id, type, route_id, depart)

    def __next_coefficients(self):
        for i in range(len(self.routes)):
            self.coefficients[i] = self.data[self.routes[i]][self.last_coefficients_id]
        self.last_coefficients_id += 1

    def next(self):
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
            for i in range(self.number):
                for route_id in range(len(self.coefficients)):
                    if random.random() < self.coefficients[route_id]:
                        print(self.__new_vehicle(vehicle_id, "type2", self.routes[route_id], i), file=routes_file)
                        vehicle_id += 1

            print("</routes>", file=routes_file)
