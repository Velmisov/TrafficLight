import sys
import subprocess
import numpy as np
import random

import traci

import settings
from models.qlearning.discrete_state import DiscreteState


class QLearning:

    def __init__(self, info, route, discount_factor: float):
        self.info = info
        self.route = route
        self.discount_factor = discount_factor

        self.discrete_state = DiscreteState(info, route)
        self.discrete_state.fit(44)

        self.actions = [settings.MIN_GREEN_TIME, 10, 15, 20, 25, 30, 35, 40, 45, 50]

        self.q_value = np.zeros((self.discrete_state.total_number_of_states, len(self.actions)))
        self.counts = np.zeros((self.discrete_state.total_number_of_states, len(self.actions)))
        self.learning_rate = np.ones((self.discrete_state.total_number_of_states, len(self.actions)))
        self.probs = np.ones((self.discrete_state.total_number_of_states, len(self.actions))) / len(self.actions)

    def compute_reward(self, queue_tracker, waiting_tracker):
        reward = 0
        for edge in self.info.EDGES_TO:
            reward -= ((1 * queue_tracker[edge]) ** 1.75 + (2 * waiting_tracker[edge]) ** 1.75)
        return reward

    def update(self, state, next_state, action, reward):
        prev_q = self.q_value[state, action]
        self.q_value[state, action] = (1 - self.learning_rate[state, action]) * prev_q + \
                                      self.learning_rate[state, action] * (reward + self.discount_factor *
                                                                     max(self.q_value[next_state, :]))
        self.counts[state, action] += 1
        self.learning_rate[state, action] = 1 / self.counts[state, action]

    def update_probs(self, state, action):
        if np.sum(self.counts[state,]) == 0 or np.sum(self.q_value[state,]) == 0:
            tau = 1
        else:
            tau = (-(np.mean(self.q_value[state,])))/(np.mean(self.counts[state,]))

        numerator = np.exp(self.q_value[state,]/tau)
        tempSum = np.sum(numerator)
        denominator = np.array([tempSum] * len(self.actions))
        self.probs[state,] = np.divide(numerator, denominator)

    def fit(self, number_of_days: int):
        port = 8813

        queue_tracker = {}
        waiting_tracker = {}
        vehicles_tracker = {}
        for edge in self.info.EDGES_TO:
            queue_tracker[edge] = 0
            waiting_tracker[edge] = 0
            vehicles_tracker[edge] = 0

        for day in range(number_of_days):
            self.route.set_coefficients([0.1, 0.1, 0.1, 0.1, 0.02, 0.02, 0.02, 0.02])
            self.route.next()
            sumo_process = subprocess.Popen(['sumo.exe', settings.WAITING_TIME_MEMORY_LIMIT,
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

                    for edge in self.info.EDGES_TO:
                        queue_tracker[edge] = traci.edge.getLastStepHaltingNumber(edge)
                        waiting_tracker[edge] = traci.edge.getWaitingTime(edge)
                        vehicles_tracker[edge] = traci.edge.getLastStepVehicleNumber(edge)

                    current_state = self.discrete_state.get_state(current_phase, queue_tracker, waiting_tracker,
                                                                  vehicles_tracker)
                    current_reward = self.compute_reward(queue_tracker, waiting_tracker)

                    if step != 0:
                        self.update(last_state, current_state, last_action, last_reward)
                        self.update_probs(last_state, last_action)

                        unigen = random.random()
                        probsActions = np.cumsum(self.probs[current_state,])

                        for i in range(len(probsActions)):
                            if unigen <= probsActions[i]:
                                current_action = i
                                break

                    # if random.random() < temperature or np.sum(self.q_value[current_state, :]) == 0:
                    #     current_action = random.randint(0, self.q_value.shape[1] - 1)
                    # else:
                    #     arg_max_array = np.argmax(self.q_value[current_state])
                    #     if type(arg_max_array) == np.int64:
                    #         arg_max_array = [arg_max_array]
                    #     else:
                    #         print(arg_max_array)
                    #     current_action = arg_max_array[random.randint(0, len(arg_max_array) - 1)]

                    traci.trafficlight.setPhaseDuration(self.info.TL, self.actions[current_action])
                    last_state = current_state
                    last_action = current_action
                    last_reward = current_reward

                traci.simulationStep()
                step += 1

            traci.close()
            sumo_process.kill()
        print(self.q_value)

    def predict(self, phase, queue, waiting, vehicles) -> int:
        state = self.discrete_state.get_state(phase, queue, waiting, vehicles)
        arg_max_array = np.argmax(self.q_value[state])
        if type(arg_max_array) == np.int64:
            arg_max_array = [arg_max_array]
        return self.actions[arg_max_array[random.randint(0, len(arg_max_array) - 1)]]

    def save(self, dir='./models/qlearning/saved/', fname='last.csv'):
        self.q_value.tofile(dir+fname, sep=',')

    def load(self, dir='./models/qlearning/saved/', fname='last.csv'):
        self.q_value = np.fromfile(dir+fname, sep=',').reshape(self.q_value.shape)
