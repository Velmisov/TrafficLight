import sys
import subprocess
import pandas as pd

import traci

import settings
from models.qlearning.discrete_state import DiscreteState


class QLearning:

    def __init__(self, info, route, learning_rate: float, discount_factor: float):
        self.info = info
        self.route = route
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_value = pd.DataFrame(columns=range(settings.MIN_GREEN_TIME, settings.MAX_GREEN_TIME))

        self.discrete_state = DiscreteState(info, route)
        self.discrete_state.fit(20)

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
        pass
        # port = 8813
        # for day in range(number_of_days):
        #     self.route.next()
        #     sumo_process = subprocess.Popen(['sumo.exe', settings.WAITING_TIME_MEMORY_LIMIT,
        #                                      "-c", self.info.PATH+".sumocfg", "--remote-port", str(port)],
        #                                     stdout=sys.stdout, stderr=sys.stderr)
        #     traci.init(port)
        #
        #     while traci.simulation.getMinExpectedNumber() > 0:
        #         traci.simulationStep()
        #
        #     traci.close()
        #     sumo_process.kill()

    def predict(self) -> int:
        pass
