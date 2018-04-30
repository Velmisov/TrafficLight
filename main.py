import os
import subprocess
import sys

import traci

import data.simple.route
import outparsing
from models.qlearning.algo import QLearning

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Undeclared environment variable 'SUMO_HOME'")

route = data.simple.route.Route(100)
parser = outparsing.Parser(route.edges)

port = 10000

for i in range(2):
    route.next()
    sumoProcess = subprocess.Popen(['sumo.exe', "--waiting-time-memory=1000000",
                                    "-c", "data\simple\simple.sumocfg", "--remote-port", str(port)],
                                   stdout=sys.stdout, stderr=sys.stderr)
    traci.init(port)

    while traci.simulation.getMinExpectedNumber() > 0:
        parser.step()
        traci.simulationStep()

    traci.close()
    sumoProcess.kill()

    parser.get_statistics()
    parser.clear()
    port += 1
