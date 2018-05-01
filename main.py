import os
import subprocess
import sys

import traci

from data.simple.route import Route
from outparsing import Parser
from models.qlearning.algo import QLearning
import settings

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Undeclared environment variable 'SUMO_HOME'")

# q = QLearning("data\simple\simple", 0.5, 0.1)
# q.fit(1)

port = 8813

route = Route(100)
parser = Parser(route.edges)

route.next()
sumo_process = subprocess.Popen(['sumo-gui.exe', settings.WAITING_TIME_MEMORY_LIMIT,
                                 "-c", "data\simple\simple.sumocfg", "--remote-port", str(port)],
                                stdout=sys.stdout, stderr=sys.stderr)
traci.init(port)

while traci.simulation.getMinExpectedNumber() > 0:
    parser.step()
    traci.simulationStep()

traci.close()
sumo_process.kill()

parser.get_statistics()
parser.clear()
