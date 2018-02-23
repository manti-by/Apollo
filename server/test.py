import time
from apollo.sensors.ili9341 import ILI9341Display as Display

display = Display(24, 25)

display.draw({'term_01': 70, 'term_02': 90, 'term_03': 20, 'water_sensor': 1})
