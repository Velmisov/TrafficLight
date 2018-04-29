import os
import sys
import subprocess
import traci
import data.simple.route

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Undeclared environment variable 'SUMO_HOME'")

route = data.simple.route.Route(100)

port = 10000

for i in range(2):
    route.next()
    sumoProcess = subprocess.Popen(['sumo-gui.exe', "-c", "data\simple\simple.sumocfg", "--remote-port", str(port)],
                                   stdout=sys.stdout, stderr=sys.stderr)
    traci.init(port)

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

    traci.close()

    port += 1
