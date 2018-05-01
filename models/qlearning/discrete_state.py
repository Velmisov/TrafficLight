import sys
import subprocess
from sklearn.cluster import KMeans

import traci

from data.simple.route import Route
import settings


class DiscreteState:

    def __init__(self, info):
        self.path = info.PATH
        self.cluster = dict()

    def fit(self, number_of_days):
        port = 8813
        route = Route(settings.CARS_IN_DAY)
        for day in range(number_of_days):
            route.next()
            sumo_process = subprocess.Popen(['sumo.exe', settings.WAITING_TIME_MEMORY_LIMIT,
                                             "-c", self.path + ".sumocfg", "--remote-port", str(port)],
                                            stdout=sys.stdout, stderr=sys.stderr)
            traci.init(port)

            while traci.simulation.getMinExpectedNumber() > 0:
                traci.simulationStep()

            traci.close()
            sumo_process.kill()

    def get_state(self):
        pass
