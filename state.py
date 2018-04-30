import traci


class State:

    def __init__(self):
        pass

    @staticmethod
    def get_waiting_time(edges):
        waiting_time = {}
        for edge in edges:
            wt = 0.
            for vehicle in traci.edge.getLastStepVehicleIDs(edge):
                wt += traci.vehicle.getAccumulatedWaitingTime(vehicle)
            waiting_time[edge] = wt
        return waiting_time

    @staticmethod
    def get_number_of_vehicles(edges):
        number = {}
        for edge in edges:
            number[edge] = len(traci.edge.getLastStepVehicleIDs(edge))
        return number
