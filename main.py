import os
import sys
import subprocess
import traci
import data.default.route

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Undeclared environment variable 'SUMO_HOME'")

data.default.route.generate()

port = 10000

sumoProcess = subprocess.Popen(['sumo-gui.exe', "-c", "data\default\default.sumocfg", "--remote-port", str(port)],
                               stdout=sys.stdout, stderr=sys.stderr)
traci.init(port)

step = 0
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    print(step)
    step += 1

traci.close()
