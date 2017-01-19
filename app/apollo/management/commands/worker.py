import logging
import RPi.GPIO as GPIO

from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from api.models import Shot
from apollo.utils import check as check_rules
from apollo.sensors.spi import read_channel as read_spi_channel
from apollo.sensors.onewire import read_channel as read_onewire_channel
from apollo.sensors.ili9341 import draw as draw_display

logger = logging.getLogger('worker')


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(settings.TERM_INPUT, GPIO.IN)
            GPIO.setup(settings.BUZZER_OUTPUT, GPIO.OUT)

            # Compile data
            data = {
                'term_01': read_onewire_channel(settings.TERM_01),
                'term_02': read_onewire_channel(settings.TERM_02),
                'term_03': read_onewire_channel(settings.TERM_03),
                'water_sensor': read_spi_channel(settings.WATER_LEVEL_INPUT),
                'created': datetime.now()
            }

            # Store data into DB
            s = Shot(**data)
            s.save()

            # Check rules and draw data
            check_rules(data, settings.BUZZER_OUTPUT)
            draw_display(data, settings.DISPLAY_POWER, settings.DISPLAY_OUTPUT)

            GPIO.cleanup()
            logging.info('Record processed')
        except Exception as e:
            logging.error(e.message)