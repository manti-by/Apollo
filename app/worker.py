import Adafruit_DHT
import datetime
import sqlite3
import spidev


DHT22_PIN = 3
SPI_CHANNEL = 1


def get_moisture_level()->int:
    spi = spidev.SpiDev()
    spi.open(0, 0)

    self.r = spi.xfer([1, (8 + self.channel) << 4, 0])
    adc_out = ((self.r[1] & 3) << 8) + self.r[2]
    percent = 100 - int(round((adc_out - 300) / 7.24))

    return percent


def get_temp_humidity()->tuple:
    return Adafruit_DHT.read_retry(
        Adafruit_DHT.DHT22, DHT22_PIN
    )


def save_data(t: float, h: int, m: int):
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS data ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "temp DECIMAL(5,2),"
            "humidity TINYINT,"
            "moisture TINYINT,"
            "datetime DATETIME"
            ");"
        )
        cursor.execute("INSERT INTO data VALUES (?, ?, ?, ?)", (
            t, h, m, datetime.datetime.now()
        ))
        connection.commit()
        connection.close()


if __name__ == '__main__':
    moisture = get_moisture_level()
    temp, humidity = get_temp_humidity()
    save_data(temp, humidity, moisture)

    print('Temp: {} *C, humidity: {}%, moisture: {}%'.format(
        temp, humidity, moisture
    ))
