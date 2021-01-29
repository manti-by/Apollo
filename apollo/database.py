import sqlite3
from decimal import Decimal

from apollo.conf import DB_PATH


def get_sensors_data() -> dict:
    with sqlite3.connect(DB_PATH) as session:
        session.row_factory = sqlite3.Row
        cursor = session.cursor()
        cursor.execute("SELECT temp, humidity, moisture, luminosity" "FROM data ORDER BY datetime DESC")
        session.commit()
        return cursor.fetchone()


def save_sensors_data(temp: int, humidity: Decimal, moisture: Decimal, luminosity: Decimal):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO data (temp, humidity, moisture, luminosity) " "VALUES (?, ?, ?, ?)",
            (temp, humidity, moisture, luminosity),
        )
        connection.commit()
