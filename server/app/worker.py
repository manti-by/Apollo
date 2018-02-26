import json
import requests

from app.db import DB
from app.conf import settings
from app.utils import get_logger
from app.sensors.ili9341 import Display

logger = get_logger()

db = DB()
result = {}
for sensor in settings['sensors']:
    r = requests.get('http://{}'.format(sensor['ip']))
    data = json.loads(r.json())
    result[sensor['name']] = data
    db.add(data)

display = Display(settings['display_dc'], settings['display_rst'])
display.draw(result)
