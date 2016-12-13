
#Copyright 2016 Ruth Ogunnaike

"""
sshscanner, this code runs 462 combinations of common weak/default usernames  and passwords against port 22 in order
to have a login access into the host. It includes method to change user's password

Procedures
runScan(IP_Address),this method initiates and run the default/weak vulnerability scanner password. The parameter
ip_address is passed as a string value.

getStatus(), this function returns the login status of the scan. The return values are Success Scan Error and Failed
. Success and Scan Error should flag the host vulnerable and the Failed status flags the host as not-vulnerable.

launchMiraiScan(IP_Address), this sends the command to run the IotSeeker program and scans for devices that still has defaults credentials
"""


from __future__ import print_function

from __future__ import absolute_import
from pexpect import pxssh
import pexpect
import os
import socket
import time
import string
import random
import subprocess
import sys, getpass

COMMAND_PROMPT = '[$#] '
TERMINAL_PROMPT = r'Terminal type\?'
TERMINAL_TYPE = 'vt100'
SSH_NEWKEY = r'Are you sure you want to continue connecting \(yes/no\)\?'

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

url = 'https://localhost:8834'

class sshscanner(object):
    def built_url(self, resource):
        return '{0}{1}'.format(url, resource)

def setStatus(value):
    global status
    status = value

def getStatus():
    return status

def launchMiraiScan(ip):
    global status
    cmd = 'perl iotScanner.pl %s' % ip
    starttime = time.time()
    mChild = pexpect.spawn('/bin/bash', ['-c',cmd], timeout = 600)
    # i = mChild.expect(['device ' + ip + ': failed to establish TCP connection',])
    i = mChild.expect(['failed to establish TCP connection', 'doesnot have any password',
                       'still has default password', 'has changed password', 'didnot find dev type after trying all devices',
                       'due to 404 response', 'failed to establish TCP connection', 'http redirect to',
                       'unexpected status code',
                       'didnot find devType for',  'unexpected partial url', TERMINAL_PROMPT, COMMAND_PROMPT])

    if i == 0:
        print('Run time:', round((time.time() - starttime),3))
        setStatus('Non-vulnerable')
    elif i == 1 or i == 2:
        setStatus('Vulnerable')
    else:
        setStatus('Non-vulnerable')


def runScan(ip):
    launchMiraiScan(ip);