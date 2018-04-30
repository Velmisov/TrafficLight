import pandas as pd
import matplotlib.pyplot as plt
from state import State


class Parser:

    def __init__(self, edges):
        self.edges = edges
        self.number_of_vehicles = pd.DataFrame(columns=edges)
        self.waiting_time = pd.DataFrame(columns=edges)

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

    def step(self):
        self.number_of_vehicles = self.number_of_vehicles.append(State.get_number_of_vehicles(self.edges),
                                                                 ignore_index=True)
        self.waiting_time = self.waiting_time.append(State.get_waiting_time(self.edges), ignore_index=True)

    def get_statistics(self):
        self.plot_number_of_vehicles()
        self.plot_waiting_time()

    def clear(self):
        self.number_of_vehicles = pd.DataFrame(columns=self.edges)
        self.waiting_time = pd.DataFrame(columns=self.edges)
