import logging.config
from typing import Tuple

import Adafruit_DHT

from apollo.conf import (
    DHT22_CHANNEL,
    LMS_CHANNEL,
    LMS_HIGH,
    LMS_LOW,
    LOGGING,
    SMS_CHANNEL,
    SMS_HIGH,
    SMS_LOW,
    SPI_DEVICE,
    SPI_PORT,
)
from apollo.database import save_sensors_data
from apollo.library import MCP3002

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

mcp3002 = MCP3002(SPI_PORT, SPI_DEVICE)


def get_moisture_level() -> float:
    adc = mcp3002.read_adc(SMS_CHANNEL)
    return round((1 - (adc - SMS_LOW) / (SMS_HIGH - SMS_LOW)) * 100, 2)


def get_luminosity_level() -> float:
    adc = mcp3002.read_adc(LMS_CHANNEL)
    return round((adc - LMS_LOW) / (LMS_HIGH - LMS_LOW) * 100, 2)


def get_temp_humidity() -> Tuple[float, int]:
     humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT22_CHANNEL)
     return round(humidity, 2), int(temp)


if __name__ == "__main__":
    moisture = get_moisture_level()
    luminosity = get_luminosity_level()
    humidity, temp = get_temp_humidity()
    save_sensors_data(temp, humidity, moisture, luminosity)

    logger.info(f"Temp: {temp} *C, humidity: {humidity}, moisture: {moisture}, luminosity: {luminosity}")

