import json

from core.conf import settings
from core.utils import node_is_live, get_mac_by_ip


# Load current sensors pool
sensors_file = open(settings['sensors_path'], 'r')
existing = json.load(sensors_file)
sensors_file.close()


# Check existing sensors are live
need_rescan = False
for sensor in settings['sensors']:
    if sensor['mac'] not in existing or not node_is_live(existing[sensor['mac']]):
        need_rescan = True


# Rescan network if needed
if need_rescan:
    result = {}
    for i in range(0, 255):
        current_ip = settings['network'].format(i)
        if node_is_live(current_ip):
            mac_address = get_mac_by_ip(current_ip)
            # if mac_address in settings['sensors']:
            result[mac_address] = current_ip

    # Save current sensors pool
    sensors_file = open(settings['sensors_path'], 'w')
    json.dump(result, sensors_file)
    sensors_file.close()
