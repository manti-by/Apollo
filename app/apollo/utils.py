import logging
import random

from datetime import tzinfo, timedelta

from django.conf import settings

from apollo.sensors.spi import read_channel as read_spi_channel
from apollo.sensors.ssd1306 import draw as draw_display, clear as clear_display
from apollo.sensors.buzzer import buzzer_short_low, buzzer_long_low, buzzer_double_short_low, \
    buzzer_double_long_low, buzzer_alert_long_low

logger = logging.getLogger('worker')


def _unique():
    return str(''.join([str(random.randint(0, 9)) for _ in range(16)]))


ZERO = timedelta(0)


class UTC(tzinfo):

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()


def test():
    try:
        clear_display(settings.DISPLAY_OUTPUT)
        level = read_spi_channel(settings.MOISTURE_INPUT)
        draw_display({
            'term_01': 90.2,
            'term_02': 87.5,
            'term_03': 34.2,
            'term_04': 29.2,
            'term_05': 7.2,
            'water_sensor': level
        }, settings.DISPLAY_OUTPUT)
        logging.info('Record processed')
    except Exception as e:
        logging.error(e.message)


def check(data, buzzer_id):
    if data['term_01'] >= 60:
        buzzer_short_low(buzzer_id)
    if data['term_01'] >= 80:
        buzzer_long_low(buzzer_id)

    if data['term_02'] >= 40:
        buzzer_double_short_low(buzzer_id)
    if data['term_02'] >= 70:
        buzzer_double_long_low(buzzer_id)
    if data['term_01'] >= 80:
        buzzer_short_low(buzzer_id)

    if data['term_03'] >= 30 or data['term_04'] >= 30 or data['term_05'] >= 30:
        buzzer_alert_long_low(buzzer_id)

    if data['water_sensor']:
        buzzer_alert_long_low(buzzer_id)
