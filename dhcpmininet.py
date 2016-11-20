#!/usr/bin/python


from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, OVSLegacyKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
import os

def topology():
    "Create a network."
    net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )

    print "*** Creating nodes"
    c1 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', port=6633 )
    s2 = net.addSwitch( 's2', listenPort=6634, mac='00:00:00:00:00:01' )
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:03', ip='no ip defined/8' )
    h2 = net.addHost( 'h2', mac='00:00:00:00:00:04', ip='no ip defined/8' )
    h3 = net.addHost( 'h3', mac='00:00:00:00:00:05', ip='no ip defined/8' )

    print "*** Creating links"
    net.addLink(h1, s2, 0, 3)
    net.addLink(h2, s2, 0, 2)
    net.addLink(h3, s2, 0, 1)

    print "*** Starting network"
    net.build()
    s2.start( [c1] )
    c1.start()

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

    clear("%s/pox/pox/firewallpolicies/firewallpolicies.csv" % os.environ['HOME'])
    clear("%s/pox/pox/firewallpolicies/whitelist.csv" % os.environ['HOME'])
    clear("%s/pox/pox/firewallpolicies/blacklist.csv" % os.environ['HOME'])

def clear(filename):
    f = open(filename, "w+")
    f.close()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()

