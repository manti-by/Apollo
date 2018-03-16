from datetime import datetime

import Adafruit_ILI9341
import Adafruit_GPIO.SPI as SPI
from PIL import Image, ImageDraw, ImageFont


class Display:

    def __init__(self, dc, rst, dt_format='%Y-%m-%d %H:%M', spi_port=0, spi_device=0):
        self.dc = dc
        self.rst = rst
        self.dt_format = dt_format

        self.spi = SPI.SpiDev(spi_port, spi_device, max_speed_hz=64000000)
        self.display = Adafruit_ILI9341.ILI9341(self.dc, rst=self.rst, spi=self.spi)
        self.dimensions = (self.display.width, self.display.height)

    def clear(self):
        self.display.begin()
        self.display.clear((0, 0, 0))

    def draw(self, data):
        self.clear()

        # Create blank image for drawing
        # Make sure to create image with mode '1' for 1-bit color
        image = Image.new('1', self.dimensions)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Write two lines of text
        line_01 = ' '
        for sensor, data in data.items():
            line_01 += '{0}: {1:.1g}/{2:.1g}  '.format(sensor, data['temp'], data['humidity'])

        updated_datetime = datetime.utcnow().strftime(self.dt_format)
        line_02 = ' Updated at {}'.format(updated_datetime)

        draw.text((2,  2), line_01, font=font, fill=255)
        draw.text((2, 18), line_02, font=font, fill=255)

        image.resize(self.dimensions)
        self.display.display(image)
