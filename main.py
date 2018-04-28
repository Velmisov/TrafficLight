
import os
import sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Undeclared environment variable 'SUMO_HOME'")

import data.simple.route

data.simple.route.generate()

port = 10000

import subprocess
import traci

sumoProcess = subprocess.Popen(['sumo-gui.exe', "-c", "data\simple\simple.sumocfg", "--remote-port", str(port)],
                               stdout=sys.stdout, stderr=sys.stderr)
traci.init(port)

step = 0
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    print(step)
    step += 1

traci.close()
