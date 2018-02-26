import json
import requests

from app.conf import settings
from app.data import DB
from app.utils import sensor_name_by_mac
from sensors.ili9341 import Display


# Load current sensors list
sensors_file = open(settings['sensors_path'], 'r')
existing = json.load(sensors_file)
sensors_file.close()


# Request sensors for data and save it to DB
db = DB()
result = {}
for mac, ip in existing:
    r = requests.get('http://{}'.format(ip))
    data = json.loads(r.json())
    result[sensor_name_by_mac(mac)] = data
    db.add(data)


# Show sensors data on display
display = Display(settings['display_dc'], settings['display_rst'])
display.draw(result)
