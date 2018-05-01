import os
import subprocess
import sys

import traci

from data.simple.route import Route
from data.simple import info
from outparsing import Parser
from models.qlearning.algo import QLearning
import settings

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Undeclared environment variable 'SUMO_HOME'")

q = QLearning(info, 0.5, 0.1)
q.fit(1)

# port = 8813
#
# route = Route(100)
# parser = Parser(info.EDGES)
#
# route.next()
# sumo_process = subprocess.Popen(['sumo-gui.exe', settings.WAITING_TIME_MEMORY_LIMIT,
#                                  "-c", "data\simple\simple.sumocfg", "--remote-port", str(port)],
#                                 stdout=sys.stdout, stderr=sys.stderr)
# traci.init(port)
#
# step = 0
# sec_in_phase = 0
# while traci.simulation.getMinExpectedNumber() > 0:
#     # print(traci.trafficlight.getPhase("tl"))
#     # if traci.trafficlight.getPhase("tl") == 0 and sec_in_phase == 0:
#     #     traci.trafficlight.setPhaseDuration("tl", 10)
#     # elif traci.trafficlight.getPhase("tl") != 0:
#     #     sec_in_phase = -1
#     parser.step()
#     traci.simulationStep()
#     step += 1
#     sec_in_phase += 1
#
# traci.close()
# sumo_process.kill()
#
# parser.get_statistics()
# parser.clear()
