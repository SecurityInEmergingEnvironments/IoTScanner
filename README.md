# IoTScanner
Utilizes an SDN to prevent IoT devices with known vulnerabilities from using the network.  The system also attempts to automatically fix vulnerabilities when possible.


To run the experiment, it is required to install the Nessus scanning tool on your virtual machine and download a mininet virtual image. You can run the experiment using only the implemented custom scanner by disabling the lines of code that launches the Nessus scanner. Read NessusScanner.py to enter the required parameters. 

Follow the steps below to run the experiment 

1.	Install Mininet VM image. Version 2.2.0 or higher
2.	In the POX controller folder in the home directory, add the following python scripts and folders in the specified directory below. Existing components in the POX server should be overwritten

Type	Name	Location
Folder	scanresults	/home/mininet/pox
Folder	firewallpolicies	/home/mininet/pox/pox
Folder	scanserver	/home/mininet/pox/pox
File	dhcpd.py	/home/mininet/pox/proto
File	dhcpmininet.py	/home/mininet/pox/topology
File	firewall.py	/home/mininet/pox/pox/misc
File	host_tracker	/home/mininet/pox/pox/host_tracker

To run the test, log into the mininet virtual machine via SSH using putty or any other suitable program. Open 3 terminals. First terminal for mininet network simulation, the second to start POX controller and the third to track the access control list
3.	To start the network simulation, enter the following commands
cd pox/pox/topology    -to go to the directory
sudo python dhcpmininet.py  - to start a network of hosts with no assigned IP_Address
sudo mn –topo single,6 - -mac - -switch ovsk  - -controller remote   -to start a network with static or pre-assigned IP_Adress

4.	To start the POX SDN controller, enter the following command;
cd pox – to go to directory
./pox.py  forwarding.l2_learning proto.dhcpd misc.firewall openflow.discovery host_tracker

This will start the POX controller and connect to the OF-switch.
5.	Go to the mininet terminal to send a dhcp request for each hosts, run 
sudo dhclient h1-eth1  (h1, h2, h3)

The POX controller terminal displays log information that displays the process currently being executed

6.	To view the access control list, enter the following command on the third terminal. 
cd pox/pox/firewallpolicies
cat whitelist.csv
cat blacklist.csv
cat firewallpolicies.csv

7.	To test the communication flow, ping hosts via the controller within the network.
 h1 ping –c1 h2
h2 ping –c1 h3   etc. 


