import time
import shutil

import scannerserver
from scannerserver import Scanner

url = 'https://localhost:8834'
verify = False
username = 'mininet'
password = 'mininetscanner'
scanResult = {}


class Interface(classmethod, Scanner):
    def __init__(self, parent=None):
        print ('login')
        # token= self.login(username, password)


def runScan(ipaddress):
    print("initiating scan")

    #print ('login')
    token = scannerserver.login(username, password)

    print('Adding new scan.')
    policies = scannerserver.get_policies(token)
    policy_id = policies['Badlock Detection']
    scan_data = scannerserver.add('Vulnerability Scan', 'Create a new scan with API', '76.103.2.54', policy_id, token)
    scan_id = scan_data['id']

    print('Updating scan with new targets.')
    scannerserver.update(scan_id, scan_data['name'], scan_data['description'], ipaddress, token)
    # '192.168.2.2
    # '173.10.208.173'
    print('Launching new scan.')
    scan_uuid = scannerserver.launch(scan_id, token)
    history_ids = scannerserver.get_history_ids(scan_id, token)
    history_id = history_ids[scan_uuid]
    while scannerserver.status(scan_id, history_id, token) != 'completed':
        time.sleep(5)

    print('Exporting the completed scan.')
    file_id = scannerserver.export(scan_id, history_id, token)
    filename = scannerserver.download(scan_id, file_id, token)
    result= scannerserver.readFile(filename)

    print(scan_id)

    print('Deleting the scan.')
    #print(scan_id)
    #print(history_id)
    # history_delete(scan_id, history_id, token)
    # delete(scan_id)
    #print('Logout')
    #print(result)
    # scanserver.logout(token)
    return result
