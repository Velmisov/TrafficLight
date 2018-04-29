import random


class Route:

    def __init__(self, number):
        self.number = number
        self.file_name = "data\simple\simple.rou.xml"
        self.types = '<vType id="type1" accel="0.8" decel="4.5" sigma="0.5" length="5" maxSpeed="70" />'
        self.routes_ids = ["route1to2", "route1to4", "route2to1", "route2to3", "route3to4",
                           "route3to1", "route4to3", "route4to2"]
        self.routes = '''<route id="route1to2" edges="1totl tlto2" />
            <route id="route1to4" edges="1totl tlto4" />
            <route id="route2to1" edges="2totl tlto1" />
            <route id="route2to3" edges="2totl tlto3" />
            <route id="route3to4" edges="3totl tlto4" />
            <route id="route3to1" edges="3totl tlto1" />
            <route id="route4to3" edges="4totl tlto3" />
            <route id="route4to2" edges="4totl tlto2" />'''

    def next(self):
        with open(self.file_name, "w") as routes_file:
            print("<routes>\n"+self.types+"\n"+self.routes, file=routes_file)

            random.seed(7)

            for i in range(self.number):
                print('<vehicle id="%d" type="type1" route="%s" depart="%d" />' %
                      (i, self.routes_ids[random.randint(0, len(self.routes_ids) - 1)], i), file=routes_file)

            print("</routes>", file=routes_file)
