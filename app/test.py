from django.conf import settings
from apollo.sensors.ili9341 import draw as draw_display

data = {'term_01': 70, 'term_02': 90, 'term_03': 20, 'water_sensor': 1}
draw_display(data, settings.DISPLAY_POWER, settings.DISPLAY_OUTPUT)
