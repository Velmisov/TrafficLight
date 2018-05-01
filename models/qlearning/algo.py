import sys
import subprocess
import pandas as pd

import traci

import settings
from data.simple.route import Route
from models.qlearning.discrete_state import DiscreteState


class QLearning:

    def __init__(self, info, learning_rate: float, discount_factor: float):
        self.path = info.PATH
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_value = pd.DataFrame(columns=range(settings.MIN_GREEN_TIME, settings.MAX_GREEN_TIME))

        self.discrete_state = DiscreteState(info)
        self.discrete_state.fit(10)

    def __print_q(self):
        print(self.q_value)

    def __reward(self, state, action) -> float:
        pass

    def __update(self, state, next_state, action):
        reward_for_state_action = self.__reward(state, action)
        prev_q = self.q_value.iloc[state, action]
        self.q_value[state, action] = prev_q + self.learning_rate * (reward_for_state_action + self.discount_factor *
                                                                     max(self.q_value[next_state, :] - prev_q))
        return self.__reward(state, action)

    def fit(self, number_of_days: int):
        self.__print_q()
        port = 8813
        route = Route(settings.CARS_IN_DAY)
        for day in range(number_of_days):
            route.next()
            sumo_process = subprocess.Popen(['sumo.exe', settings.WAITING_TIME_MEMORY_LIMIT,
                                             "-c", self.path+".sumocfg", "--remote-port", str(port)],
                                            stdout=sys.stdout, stderr=sys.stderr)
            traci.init(port)

            while traci.simulation.getMinExpectedNumber() > 0:
                traci.simulationStep()

            traci.close()
            sumo_process.kill()

    def predict(self) -> int:
        pass
