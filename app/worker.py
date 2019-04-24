import os

import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

from db import save_data

SPI_PORT = 0
SPI_DEVICE = 0

MOISTURE_CHANNEL = 0
LUMINOSITY_CHANNEL = 1
DHT22_CHANNEL = 4

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db.sqlite")


def get_mcp3008_input_value(input_channel) -> int:
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    adc = mcp.read_adc(input_channel)
    return 100 - adc / 10.24


def get_moisture_level() -> int:
    return get_mcp3008_input_value(MOISTURE_CHANNEL)


def get_luminosity_level() -> int:
    return get_mcp3008_input_value(LUMINOSITY_CHANNEL)


def get_temp_humidity() -> tuple:
    return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT22_CHANNEL)


if __name__ == "__main__":
    moisture = get_moisture_level()
    luminosity = get_luminosity_level()
    humidity, temp = get_temp_humidity()
    save_data(temp, humidity, moisture, luminosity)

    print(
        "Temp: {:0.2f} *C, humidity: {:d}%, moisture: {:d}%, luminosity: {:d}%".format(
            temp, int(humidity), int(moisture), int(luminosity)
        )
    )
