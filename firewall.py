
from pox.core import core
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr,EthAddr,parse_cidr
from collections import namedtuple

import pox.openflow.libopenflow_01 as of
import os
from  csv import DictReader

log = core.getLogger()
policydoc = "pox/firewallpolicies/firewallpolicies.csv"

# Policy is data structure which contains a single
# source-destination flow to be blocked on the controller.
Policy = namedtuple('Policy', ('dl_src', 'dl_dst'))


class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
	core.openflow.addListeners(self, "all")
        log.debug("Enabling Firewall")

    def read_policies(self, file):
        with open(file, 'r') as f:
            reader = DictReader(f, delimiter=",")
            policies = {}
            for row in reader:
                policies[row['id']] = Policy(EthAddr(row['mac_0']), EthAddr(row['mac_1']))
        return policies

    def _handle_ConnectionUp(self, event):
        policies = self.read_policies(policydoc)
        for policy in policies.itervalues():

            # create generic table entry
            msg = of.ofp_flow_mod()
            msg.priority = 20
            msg.actions.append(of.ofp_action_output(port=of.OFPP_NONE))

            # create match
            match = of.ofp_match()

            # Unidirectional
            match.dl_src = policy.dl_src
            match.dl_dst = policy.dl_dst
            msg.match = match
            event.connection.send(msg)

            # Bidirecional
            match.dl_src = policy.dl_dst
            match.dl_dst = policy.dl_src
            msg.match = match
            event.connection.send(msg)

            log.info("Installing firewall policy for src=%s, dst=%s" % (policy.dl_src, policy.dl_dst))
            log.debug(msg)

        log.info("Routing %s", dpidToStr(event.dpid))

        log.debug("Firewall policy installed on %s", dpidToStr(event.dpid))


def launch():
    '''Start the Firewall '''
    core.registerNew(Firewall)
