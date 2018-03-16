import json
import requests

from core.conf import settings
from core.database import DB
from core.utils import sensor_name_by_mac, get_logger, get_debug_response
from sensors.ili9341 import Display

logger = get_logger()


# Load current sensors list
sensors_file = open(settings['sensors_path'], 'r')
existing = json.load(sensors_file)
sensors_file.close()


# Request sensors for data and save it to DB
db = DB()
result = {}
for mac, ip in existing.items():
    if settings['debug']:
        data = get_debug_response()
    else:
        try:
            r = requests.get('http://{}'.format(ip))
            data = json.loads(r.json())
            if r.status_code != 200 or data['result'] != 200:
                reason = r.reason if r.status_code != 200 else data['message']
                logger.error('Get data for sensor {} failed [{}]'.format(mac, reason))
                continue
        except Exception as e:
            logger.error('Unhandled exception [{}]'.format(e))
            continue

    # Append data to db and result dict for display
    result[sensor_name_by_mac(mac)] = data['data']
    data['data']['mac'] = mac
    db.add(data['data'])


# Show sensors data on display
display = Display(settings['display_dc'], settings['display_rst'], settings['dt_format'])
display.draw(result)
