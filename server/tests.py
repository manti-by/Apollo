from time import sleep

from app.conf import settings
from sensors.ili9341 import Display

display = Display(settings['display_dc'], settings['display_rst'])

data = {'Test Sensor': {'mac': '00:00:00:00:00:00', 'temp': 22.5, 'humidity': 45.4}}
display.draw(data)

sleep(5)
display.clear()
