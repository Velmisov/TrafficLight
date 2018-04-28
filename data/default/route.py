
def generate():
    n = 200
    with open("data\default\default.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="type1" accel="0.8" decel="4.5" sigma="0.5" length="5" maxSpeed="70" />
        <route id="route1to2" color="1,1,0" edges="1totl tlto2" />
        <route id="route1to4" color="1,1,0" edges="1totl tlto4" />
        <route id="route1to3" color="1,1,0" edges="1totl tlto3" />
        <route id="route2to1" color="1,1,0" edges="2totl tlto1" />
        <route id="route2to3" color="1,1,0" edges="2totl tlto3" />
        <route id="route2to4" color="1,1,0" edges="2totl tlto4" />
        <route id="route3to4" color="1,1,0" edges="3totl tlto4" />
        <route id="route3to1" color="1,1,0" edges="3totl tlto1" />
        <route id="route3to2" color="1,1,0" edges="3totl tlto2" />
        <route id="route4to3" color="1,1,0" edges="4totl tlto3" />
        <route id="route4to2" color="1,1,0" edges="4totl tlto2" />
        <route id="route4to1" color="1,1,0" edges="4totl tlto1" />
        """, file=routes)

        routes_ids = ["route1to2", "route1to3", "route1to4", "route2to1", "route2to3", "route2to4", "route3to1",
                      "route3to2", "route3to4", "route4to1", "route4to2", "route4to3"]
        import random
        random.seed(7)

        for i in range(n):
            print('<vehicle id="%d" type="type1" route="%s" depart="%d" color="1,0,0" />' %
                  (i, routes_ids[random.randint(0, 11)], i), file=routes)

        print("</routes>", file=routes)
