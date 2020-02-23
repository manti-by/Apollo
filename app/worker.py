import Adafruit_DHT

from app.conf import (DHT22_CHANNEL, LMS_CHANNEL, LMS_HIGH, LMS_LOW,
                      SMS_CHANNEL, SMS_HIGH, SMS_LOW, SPI_DEVICE, SPI_PORT)
from app.database import save_data
from app.library import MCP3002

mcp3002 = MCP3002(SPI_PORT, SPI_DEVICE)


def get_moisture_level() -> int:
    adc = mcp3002.read_adc(SMS_CHANNEL)
    return int((1 - (adc - SMS_LOW) / (SMS_HIGH - SMS_LOW)) * 100)


def get_luminosity_level() -> int:
    adc = mcp3002.read_adc(LMS_CHANNEL)
    return int((adc - LMS_LOW) / (LMS_HIGH - LMS_LOW) * 100)


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
