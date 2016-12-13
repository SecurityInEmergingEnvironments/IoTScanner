
# Copyright 2016 Ruth Ogunnaike
"""

provides the interface to initiate vulnerability scan. Multiple scans can be launched from this interface.
Add your custom scanner to use this interface.
runScan, this runs vulnerabilities scans using the integrated scanning tools (both penetration testing tools and
custom scanners based on your configuration).Your scanner must be configured to return Vulnerable or Non-vulnerable
getStatus(), this returns a scan status Vulnerable or Non-vulnerable after analyzing results from all the integrated
scanning tools. If >50% of the tools flags the device as Vulnerable, the final status will be Vulnerable. If <50%,
flagged as non-vulnerable. (The percentage can vary depending on our digression)
isResolved(ip), this tries to resolve the vulnerabilities detected. Currently, it only resolves for default or weak passwo
rd vulnerability

updateList(directory, mac_add) blacklists or whitelists the device based on the scan status. The directory is the black
list or white list directory. Mac_add is the MAC address of the device

updatePolicy(whitelist, blacklist, firewallpolicies), this method update the firewall policies (the access control list)
.Blacklisted hosts are blocked from communicating with other hosts in the network. Parameter whitelistis the whitelisted
hosts file director, blacklist is the blacklisted hosts file director and firewallpolicies is the access control list file directory.
 """
import NessusScanner
import SshScanner
import UpdatePolicy
import MiraiScanner

class ScanInterface(classmethod):
    def __init__(self, parent=None):
        print ('login')
        # token= self.login(username, password)


def runScan(ip):
    print(ip)
    MiraiScanner.runScan(ip)
    #SshScanner.runScan(ip)
    #NessusScanner.runScan(ip)
    #print ("this")


def getStatus():
    #global value
    value = 0
    status = MiraiScanner.getStatus()
    #status = status + ',' + NessusScanner.getStatus() + ',' + MiraiScanner.getStatus()
    ScanStatus = status.split(',')
    count = len(ScanStatus)
    print (count)

    for i in range(0, count):
        if(ScanStatus[i] == 'Vulnerable'):
            value += 1
        else:
            value += 0
    percent =round(((value / count ) * 100),2)

    if (percent > 20):
        return 'Vulnerable'
    else:
        return 'Non-vulnerable'


def isResolved(ip):
    SshScanner.isPasswordChanged(ip)

def updateList(directory, mac_add):
    UpdatePolicy.addlist(directory, mac_add)

def updatePolicy(whitelist, blacklist, firewallpolicies):
    UpdatePolicy.updatepolicy(whitelist, blacklist, firewallpolicies)

def exist(directory, mac_add):
    UpdatePolicy.exist(directory, mac_add)
