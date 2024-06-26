from network_topology import NetworkTopology
from network_traffic import NetworkTraffic
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.clean import Cleanup
from mininet.node import RemoteController
from mininet.util import dumpNodeConnections
import utils
import time
from utils import costants

def main():
    #Create a network topology object
    topology = NetworkTopology()
    
    #Create a Mininet object
    print("\n\n{}  {}NETWORK {}Creating Mininet network{}\n\n".format(costants['net_emote'], costants['ansi_red'],costants['ansi_white'],costants['ansi_white']))
    network = Mininet(topology,controller=None,autoSetMacs=True,autoStaticArp=True)

    #add the controller
    network.addController("LoadBalancerController",ip=costants['controller_host'],port=costants['controller_port'],controller=RemoteController)
    #Start the network
    network.start()
    #Dump the connections
    dumpNodeConnections(network.hosts)
    print("\n\n{}  {}NETWORK {}Network started{}".format(costants['net_emote'], costants['ansi_green'],costants['ansi_white'],costants['ansi_white']))

    #Create a network traffic object
    traffic_controller = NetworkTraffic(network,topology)

    #Ping all the hosts to check the reachability
    traffic_controller.ping_all()

    time.sleep(2)
    #Generate traffic between all the hosts
    traffic_controller.generate_all_traffic()

    #Open the Mininet CLI
    CLI(network)

if __name__ == "__main__":
    setLogLevel('info')
    #remove any existing Mininet instances
    print("{}  {}CLEANUP {} Removing any existing Mininet instances{}\n\n".format(costants['important_emote'], costants['ansi_red'],costants['ansi_white'],costants['ansi_white']))
    Cleanup.cleanup()
    print("\n\n{}  {}CLEANUP {} Mininet instances removed{}".format(costants['important_emote'], costants['ansi_green'],costants['ansi_white'],costants['ansi_white']))

    #wait until the controller is up
    while True:
        if utils.port_scan(costants['controller_host'],costants['controller_port']):
            break
        print("{}  {}WAIT {} Waiting for the controller to start{}".format(costants['important_emote'], costants['ansi_red'],costants['ansi_white'],costants['ansi_white']))
        time.sleep(2)
    print("\n\n{}  {}WAIT {} Controller is up and running{}".format(costants['important_emote'], costants['ansi_green'],costants['ansi_white'],costants['ansi_white']))
    main()