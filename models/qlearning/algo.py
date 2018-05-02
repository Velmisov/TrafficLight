import sys
import subprocess
import numpy as np
import random

import traci

import settings
from models.qlearning.discrete_state import DiscreteState


class QLearning:

    def __init__(self, info, route, learning_rate: float, discount_factor: float):
        self.info = info
        self.route = route
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        self.discrete_state = DiscreteState(info, route)
        self.discrete_state.fit(20)

        self.q_value = np.zeros((self.discrete_state.total_number_of_states,
                                 settings.MAX_GREEN_TIME - settings.MIN_GREEN_TIME))

    def __print_q(self):
        print(self.q_value)

    def __compute_reward(self, queue_tracker, waiting_tracker):
        reward = 0
        for edge in self.info.EDGES:
            reward -= ((1 * queue_tracker[edge]) ** 1.75 + (2 * waiting_tracker[edge]) ** 1.75)
        return reward

    def __update(self, state, next_state, action, reward):
        prev_q = self.q_value[state, action]
        self.q_value[state, action] = prev_q + self.learning_rate * (reward + self.discount_factor *
                                                                     max(self.q_value[next_state, :] - prev_q))

    def fit(self, number_of_days: int):
        port = 8813

        queue_tracker = {}
        waiting_tracker = {}
        vehicles_tracker = {}
        for edge in self.info.EDGES:
            queue_tracker[edge] = 0
            waiting_tracker[edge] = 0
            vehicles_tracker[edge] = 0

        temperature = 1.
        for day in range(number_of_days):
            self.route.set_coefficients([0.25, 0.25, 0.25, 0.25, 0., 0., 0., 0.])
            self.route.next()
            sumo_process = subprocess.Popen(['sumo-gui.exe', settings.WAITING_TIME_MEMORY_LIMIT,
                                             "-c", self.info.PATH+".sumocfg", "--remote-port", str(port)],
                                            stdout=sys.stdout, stderr=sys.stderr)
            traci.init(port)

            step = 0
            current_phase = int(traci.trafficlight.getPhase(self.info.TL))
            time_current_phase = 0
            current_state = -1
            last_state = -1
            current_action = -1
            last_action = -1
            current_reward = -1
            last_reward = -1
            while traci.simulation.getMinExpectedNumber() > 0:

                if current_phase == int(traci.trafficlight.getPhase(self.info.TL)) and step != 0:
                    time_current_phase += 1
                else:
                    time_current_phase = 0
                    current_phase = int(traci.trafficlight.getPhase(self.info.TL))

                if current_phase in self.info.GREEN_PHASES and time_current_phase == 0:

                    for edge in self.info.EDGES:
                        queue_tracker[edge] = traci.edge.getLastStepHaltingNumber(edge)
                        waiting_tracker[edge] = traci.edge.getWaitingTime(edge)
                        vehicles_tracker[edge] = traci.edge.getLastStepVehicleNumber(edge)

                    current_state = self.discrete_state.get_state(current_phase, queue_tracker, waiting_tracker,
                                                                  vehicles_tracker)
                    current_reward = self.__compute_reward(queue_tracker, waiting_tracker)

                    if step != 0:
                        self.__update(last_state, current_state, last_action, last_reward)

                    if random.random() < temperature or np.sum(self.q_value[current_state, :]) == 0:
                        current_action = random.randint(0, self.q_value.shape[1] - 1)
                    else:
                        arg_max_array = np.argmax(self.q_value[current_state])
                        if type(arg_max_array) == np.int64:
                            arg_max_array = [arg_max_array]
                        else:
                            print(arg_max_array)
                        current_action = arg_max_array[random.randint(0, len(arg_max_array) - 1)]

                    traci.trafficlight.setPhaseDuration(self.info.TL, settings.MIN_GREEN_TIME + current_action)
                    last_state = current_state
                    last_action = current_action
                    last_reward = current_reward
                    temperature = max(0.01, temperature - 0.001)

                traci.simulationStep()
                step += 1

            traci.close()
            sumo_process.kill()
        print(self.q_value)
        print(temperature)

    def predict(self, phase, queue, waiting, vehicles) -> int:
        state = self.discrete_state.get_state(phase, queue, waiting, vehicles)
        arg_max_array = np.argmax(self.q_value[state])
        if type(arg_max_array) == np.int64:
            arg_max_array = [arg_max_array]
        return arg_max_array[random.randint(0, len(arg_max_array) - 1)]
