import traci
import pandas as pd
import matplotlib.pyplot as plt
from state import State


class Parser:

    def __init__(self, edges):
        self.edges = edges
        self.number_of_vehicles = pd.DataFrame(columns=edges)
        self.waiting_time = pd.DataFrame(columns=edges)
        self.total_waiting_time = pd.DataFrame(columns=["TotalWaitingTime"])
        self.vehicles_accumulated_waiting_time = {}

    def plot_waiting_time(self):
        self.waiting_time.groupby(self.waiting_time.index).sum().plot()

        plt.xlabel("Total time")
        plt.ylabel("Waiting time")
        plt.title("Waiting time for edges")
        plt.show()

    def plot_number_of_vehicles(self):
        self.number_of_vehicles.groupby(self.number_of_vehicles.index).sum().plot()

        plt.xlabel("Total time")
        plt.ylabel("Number of vehicles")
        plt.title("Number of vehicles for edges")
        plt.show()

    def plot_total_waiting_time(self):
        self.total_waiting_time.groupby(self.total_waiting_time.index).sum().plot()

        plt.xlabel("Total time")
        plt.ylabel("Total waiting time")
        plt.title("Progress of total waiting time")
        plt.show()

    def step(self):
        self.number_of_vehicles = self.number_of_vehicles.append(State.get_number_of_vehicles(self.edges),
                                                                 ignore_index=True)
        self.waiting_time = self.waiting_time.append(State.get_waiting_time(self.edges), ignore_index=True)

        for edge in self.edges:
            for vehicle in traci.edge.getLastStepVehicleIDs(edge):
                self.vehicles_accumulated_waiting_time[vehicle] = traci.vehicle.getAccumulatedWaitingTime(vehicle)
        current_sum_of_waiting_time = 0.
        for waiting_time in self.vehicles_accumulated_waiting_time.values():
            current_sum_of_waiting_time += waiting_time
        self.total_waiting_time = self.total_waiting_time.append({"TotalWaitingTime": current_sum_of_waiting_time},
                                                                 ignore_index=True)

    def get_statistics(self):
        self.plot_number_of_vehicles()
        self.plot_waiting_time()
        self.plot_total_waiting_time()

    def clear(self):
        self.number_of_vehicles = pd.DataFrame(columns=self.edges)
        self.waiting_time = pd.DataFrame(columns=self.edges)
        self.total_waiting_time = pd.DataFrame(columns=["TotalWaitingTime"])
        self.vehicles_accumulated_waiting_time = {}
