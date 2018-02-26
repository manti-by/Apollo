import json

from app.conf import settings
from app.utils import node_is_live, get_mac_by_ip


# Load current sensors pool
sensors_file = open(settings['sensors_path'], 'r')
existing = json.load(sensors_file)
sensors_file.close()


# Check existing sensors are live
need_rescan = False
for sensor in settings['sensors']:
    if sensor['mac'] not in existing or not node_is_live(existing[sensor['mac']]):
        need_rescan = False


# Rescan network if needed
if need_rescan:
    result = {}
    for i in range(0, 255):
        current_ip = '192.168.0.{}'.format(i)
        if node_is_live(current_ip):
            mac_address = get_mac_by_ip(current_ip)
            if mac_address in settings['sensors']:
                result[mac_address] = current_ip

    # Save current sensors pool
    sensors_file = open(settings['sensors_path'], 'w')
    json.dump(sensors_file, result)
    sensors_file.close()
