import os
import sys
import subprocess
import traci
import data.simple.route
from outparsing import Parser
from state import State
import pandas as pd

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Undeclared environment variable 'SUMO_HOME'")

route = data.simple.route.Route(1000)

port = 10000

for i in range(1):
    route.next()
    sumoProcess = subprocess.Popen(['sumo-gui.exe', "-c", "data\simple\simple.sumocfg", "--remote-port", str(port)],
                                   stdout=sys.stdout, stderr=sys.stderr)
    traci.init(port)

    number_of_vehicles = pd.DataFrame(columns=route.edges)
    waiting_time = pd.DataFrame(data=[], columns=route.edges)
    # total_waiting_time = pd.DataFrame(data=[], columns=route.edges)

    while traci.simulation.getMinExpectedNumber() > 0:
        number_of_vehicles = number_of_vehicles.append(State.get_number_of_vehicles(route.edges), ignore_index=True)
        waiting_time = waiting_time.append(State.get_waiting_time(route.edges), ignore_index=True)
        # total_waiting_time = total_waiting_time.append(current_total_time, ignore_index=True)

        traci.simulationStep()

    Parser.plot_number_of_vehicles(number_of_vehicles)
    Parser.plot_waiting_time(waiting_time)
    # Parser.plot_total_waiting_time(total_waiting_time)

    traci.close()

    port += 1
