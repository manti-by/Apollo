from datetime import datetime

import Adafruit_ILI9341
import Adafruit_GPIO.SPI as SPI
from PIL import Image, ImageDraw, ImageFont

from app.conf import settings
from app.utils import get_logger

logger = get_logger()


class Display:

    def __init__(self, dc, rst):
        self.dc = dc
        self.rst = rst

    def clear(self):
        try:
            # Initialize library
            display = Adafruit_ILI9341.ILI9341(self.dc, rst=self.rst,
                                               spi=SPI.SpiDev(0, 0, max_speed_hz=64000000))
            display.begin()
            display.clear((0, 0, 0))
        except Exception as e:
            logger.error(e)

    def draw(self, data):
        try:
            # Initialize library
            display = Adafruit_ILI9341.ILI9341(self.dc, rst=self.rst,
                                               spi=SPI.SpiDev(0, 0, max_speed_hz=64000000))
            display.begin()
            display.clear((0, 0, 0))

            # Create blank image for drawing
            # Make sure to create image with mode '1' for 1-bit color
            image = Image.new('1', (display.width, display.height))
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()

            # Write two lines of text
            line_01 = ' '
            for sensor, data in data:
                line_01 += '{}: {0:.2g}/{:d}  '.format(sensor, data['temp'], data['humidity'])

            dt = datetime.utcnow().strftime(settings['dt_format'])
            line_02 = ' Updated at {}'.format(dt)

            draw.text((2,  2), line_01, font=font, fill=255)
            draw.text((2, 18), line_02, font=font, fill=255)

            display.display(image)
        except Exception as e:
            logger.error(e)
