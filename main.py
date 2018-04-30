import os
import sys
import subprocess
import traci
import data.simple.route
import outparsing
from state import State
import pandas as pd

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Undeclared environment variable 'SUMO_HOME'")

route = data.simple.route.Route(200)
parser = outparsing.Parser(route.edges)

port = 10000

for i in range(3):
    route.next()
    sumoProcess = subprocess.Popen(['sumo-gui.exe', "-c", "data\simple\simple.sumocfg", "--remote-port", str(port)],
                                   stdout=sys.stdout, stderr=sys.stderr)
    traci.init(port)

    while traci.simulation.getMinExpectedNumber() > 0:
        parser.step()
        traci.simulationStep()

    traci.close()

    parser.get_statistics()
    parser.clear()
    port += 1
