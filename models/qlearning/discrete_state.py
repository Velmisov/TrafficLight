import sys
import subprocess
import numpy as np
from sklearn.cluster import KMeans
from pathlib import Path
import os
import pickle

import traci

import settings


class DiscreteState:

    def __init__(self, info, route):
        self.info = info
        self.route = route
        self.cluster = {}
        self.number_of_clusters = 50
        self.actually_state = {}
        self.total_number_of_states = 0

    def __make_actually_states(self):
        current_state = 0
        for phase in self.info.GREEN_PHASES:
            self.actually_state[phase] = {}
            for state in range(self.number_of_clusters):
                self.actually_state[phase][state] = current_state
                current_state += 1
        self.total_number_of_states = current_state

    def fit(self, number_of_days):
        if Path(self.info.DIR+"cluster").is_dir():
            ok = True
            for phase in self.info.GREEN_PHASES:
                if not Path(self.info.DIR+"cluster\phase"+str(phase)+".sav").exists():
                    ok = False
            if ok:
                for phase in self.info.GREEN_PHASES:
                    self.cluster[phase] = pickle.load(open(self.info.DIR+"cluster\phase"+str(phase)+".sav", "rb"))
                self.__make_actually_states()
                return

        data = {}
        for i in self.info.GREEN_PHASES:
            data[i] = np.array([])

        queue_tracker = {}
        waiting_tracker = {}
        vehicles_tracker = {}
        for edge in self.info.EDGES_TO:
            queue_tracker[edge] = 0
            waiting_tracker[edge] = 0
            vehicles_tracker[edge] = 0

        port = 8813
        for day in range(number_of_days):
            self.route.next()
            sumo_process = subprocess.Popen(['sumo.exe', settings.WAITING_TIME_MEMORY_LIMIT,
                                             "-c", self.info.PATH+".sumocfg", "--remote-port", str(port)],
                                            stdout=sys.stdout, stderr=sys.stderr)
            traci.init(port)

            step = 0
            current_phase = int(traci.trafficlight.getPhase(self.info.TL))
            time_current_phase = 0
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

                    new_data = []
                    for edge in self.info.EDGES_TO:
                        new_data.append(queue_tracker[edge])
                    for edge in self.info.EDGES_TO:
                        new_data.append(waiting_tracker[edge])
                    for edge in self.info.EDGES_TO:
                        new_data.append(vehicles_tracker[edge])

                    if len(data[current_phase]) == 0:
                        data[current_phase] = np.array(new_data)
                    else:
                        data[current_phase] = np.vstack([data[current_phase], new_data])
                traci.simulationStep()
                step += 1

            traci.close()
            sumo_process.kill()

        if not Path(self.info.DIR+"cluster").is_dir():
            os.mkdir(self.info.DIR+"cluster")
        for phase in self.info.GREEN_PHASES:
            self.cluster[phase] = KMeans(n_clusters=self.number_of_clusters)
            self.cluster[phase].fit(data[phase])
            pickle.dump(self.cluster[phase], open(self.info.DIR+"cluster\phase"+str(phase)+".sav", "wb"))

        self.__make_actually_states()

    def get_state(self, phase, queue, waiting, vehicles):
        state = []
        for edge in self.info.EDGES_TO:
            state.append(queue[edge])
        for edge in self.info.EDGES_TO:
            state.append(waiting[edge])
        for edge in self.info.EDGES_TO:
            state.append(vehicles[edge])
        state = np.array(state)
        return self.actually_state[phase][self.cluster[phase].predict(state.reshape(1, -1))[0]]
