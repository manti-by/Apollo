import logging.config
from decimal import Decimal
from typing import Tuple

import Adafruit_DHT

from apollo.conf import (DHT22_CHANNEL, LMS_CHANNEL, LMS_HIGH, LMS_LOW,
                         LOGGING, SMS_CHANNEL, SMS_HIGH, SMS_LOW, SPI_DEVICE,
                         SPI_PORT)
from apollo.database import save_sensors_data
from apollo.library import MCP3002

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

mcp3002 = MCP3002(SPI_PORT, SPI_DEVICE)


def get_moisture_level() -> Decimal:
    adc = mcp3002.read_adc(SMS_CHANNEL)
    return Decimal((1 - (adc - SMS_LOW) / (SMS_HIGH - SMS_LOW)) * 100)


def get_luminosity_level() -> Decimal:
    adc = mcp3002.read_adc(LMS_CHANNEL)
    return Decimal((adc - LMS_LOW) / (LMS_HIGH - LMS_LOW) * 100)


def get_temp_humidity() -> Tuple[Decimal, int]:
    return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT22_CHANNEL)


if __name__ == "__main__":
    moisture = get_moisture_level()
    luminosity = get_luminosity_level()
    humidity, temp = get_temp_humidity()
    save_sensors_data(temp, humidity, moisture, luminosity)

    message = "Temp: {:0.2f} *C, humidity: {:d}%, moisture: {:d}%, luminosity: {:d}%"
    logger.info(message.format(int(temp), Decimal(humidity), Decimal(moisture), Decimal(luminosity)))
