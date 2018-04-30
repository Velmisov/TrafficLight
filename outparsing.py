import pandas as pd
import matplotlib.pyplot as plt


class Parser:

    def __init__(self):
        pass

    @staticmethod
    def plot_waiting_time(waiting_time: pd.DataFrame):
        waiting_time.groupby(waiting_time.index).sum().plot()

        plt.xlabel("Total time")
        plt.ylabel("Waiting time")
        plt.title("Waiting time for edges")
        plt.show()

    @staticmethod
    def plot_number_of_vehicles(number: pd.DataFrame):
        number.groupby(number.index).sum().plot()

        plt.xlabel("Total time")
        plt.ylabel("Number of vehicles")
        plt.title("Number of vehicles for edges")
        plt.show()

    @staticmethod
    def plot_total_waiting_time(total_waiting_time: pd.DataFrame):
        total_waiting_time.groupby(total_waiting_time.index).sum().plot()

        plt.xlabel("Total time")
        plt.ylabel("Total waiting time")
        plt.title("Total waiting time for edges")
        plt.show()
