import sqlite3

from apollo.conf import DB_PATH


def get_weather_data() -> dict:
    with sqlite3.connect(DB_PATH) as session:
        session.row_factory = sqlite3.Row
        cursor = session.cursor()
        cursor.execute(
            "SELECT temp, pressure, icon, wind_speed, wind_direction, datetime "
            "FROM weather ORDER BY datetime DESC",
        )
        session.commit()
        return dict(cursor.fetchone())


def save_weather_data(
    temp: float, pressure: int, icon: str, wind_speed: int, wind_deg: int
):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO weather (temp, pressure, icon, wind_speed, wind_direction) "
            "VALUES (?, ?, ?, ?, ?)",
            (temp, pressure, icon, wind_speed, wind_deg),
        )
        connection.commit()
