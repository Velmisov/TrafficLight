import sys
import subprocess

import traci

import settings
from data.simple.route import Route
import models.qlearning.discrete_state


class QLearning:

    def __init__(self, path: str):
        self.path = path

    def fit(self, number_of_days: int):
        port = 5000
        route = Route(settings.CARS_IN_DAY)
        for day in range(number_of_days):
            route.next()
            sumo_process = subprocess.Popen(['sumo.exe', "--waiting-time-memory=1000000",
                                             "-c", self.path+".sumocfg", "--remote-port", str(port)],
                                            stdout=sys.stdout, stderr=sys.stderr)
            traci.init(port)

            while traci.simulation.getMinExpectedNumber() > 0:
                traci.simulationStep()

            traci.close()
            sumo_process.kill()

    def predict(self) -> int:
        pass
