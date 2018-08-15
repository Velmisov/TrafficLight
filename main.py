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

q = QLearning(info, Route(settings.CARS_IN_DAY * 6), 0.95)
q.fit(5)

route = Route(settings.CARS_IN_DAY)
route.set_coefficients([0.1, 0.1, 0.1, 0.1, 0.02, 0.02, 0.02, 0.02])
port = 8814

parser = Parser(info.EDGES)

route.next()
sumo_process = subprocess.Popen(['sumo-gui.exe', settings.WAITING_TIME_MEMORY_LIMIT,
                                 "-c", "data\simple\simple.sumocfg", "--remote-port", str(port)],
                                stdout=sys.stdout, stderr=sys.stderr)
traci.init(port)

step = 0
current_phase = int(traci.trafficlight.getPhase(info.TL))
sec_in_phase = 0
queue_tracker = {}
waiting_tracker = {}
vehicles_tracker = {}
while traci.simulation.getMinExpectedNumber() > 0:
    if current_phase == int(traci.trafficlight.getPhase(info.TL)) and step != 0:
        time_current_phase += 1
    else:
        time_current_phase = 0
        current_phase = int(traci.trafficlight.getPhase(info.TL))

    if current_phase in info.GREEN_PHASES and time_current_phase == 0:

        for edge in info.EDGES:
            queue_tracker[edge] = traci.edge.getLastStepHaltingNumber(edge)
            waiting_tracker[edge] = traci.edge.getWaitingTime(edge)
            vehicles_tracker[edge] = traci.edge.getLastStepVehicleNumber(edge)

        time_duration = q.predict(current_phase, queue_tracker, waiting_tracker, vehicles_tracker)
        traci.trafficlight.setPhaseDuration(info.TL, time_duration)
        print(current_phase, time_duration)

    parser.step()
    traci.simulationStep()
    step += 1
    sec_in_phase += 1

traci.close()
sumo_process.kill()

parser.get_statistics()
parser.clear()
