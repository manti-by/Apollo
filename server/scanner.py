import json

from core.conf import settings
from core.utils import node_is_live, get_mac_by_ip, get_logger

logger = get_logger()


# Load current sensors pool
sensors_file = open(settings['sensors_path'], 'r')
existing = json.load(sensors_file)
sensors_file.close()


# Check existing sensors are live
need_rescan = False
for mac, name in settings['sensors'].items():
    if mac not in existing or not node_is_live(existing[mac]):
        need_rescan = True


# Rescan network if needed
if need_rescan:
    result = {}
    for i in range(0, 255):
        current_ip = settings['network'].format(i)
        if node_is_live(current_ip):
            mac_address = get_mac_by_ip(current_ip)
            if mac_address is None:
                logger.warning('Cant get mac address for ip {}'.format(current_ip))
                continue

            # Update ip for sensor mac address
            if mac_address in settings['sensors'] or settings['debug']:
                result[mac_address] = current_ip

    # Save current sensors pool
    sensors_file = open(settings['sensors_path'], 'w')
    json.dump(result, sensors_file)
    sensors_file.close()
