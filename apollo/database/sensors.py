import sqlite3

from datetime import datetime
from pytz import utc

from apollo.conf import DB_PATH, PERIODS, DT_FORMAT, LOCAL_TZ


def get_sensors_data(limit: int = None, group: str = None) -> dict:
    limit = limit if limit is not None else 10
    group = group if group is not None else "hourly"

    with sqlite3.connect(DB_PATH) as session:
        session.row_factory = sqlite3.Row
        cursor = session.cursor()
        query_limit = PERIODS.get(group, 1) * int(limit)
        cursor.execute(
            "SELECT temp, humidity, moisture, luminosity, datetime "
            "FROM data ORDER BY datetime DESC LIMIT ?",
            (query_limit,),
        )
        session.commit()
        data = cursor.fetchall()[::-1]

        result = {
            "temp": [],
            "humidity": [],
            "moisture": [],
            "luminosity": [],
            "label": [],
        }

        sum_temp = 0
        sum_humidity = 0
        sum_moisture = 0
        sum_luminosity = 0
        counter = 0

        period = PERIODS.get(group)
        for item in data:
            counter += 1
            sum_temp += item["temp"] or 0
            sum_humidity += item["humidity"] or 0
            sum_moisture += item["moisture"] or 0
            sum_luminosity += item["luminosity"] or 0

            timestamp = utc.localize(
                datetime.strptime(item["datetime"], DT_FORMAT), is_dst=None
            ).astimezone(LOCAL_TZ)

            if group in ("live", "hourly"):
                label = timestamp.strftime("%H:%M")
            else:
                label = timestamp.strftime("%Y-%m-%d")

            if period is None:
                continue

            if counter % period == 0:
                result["temp"].append(round(sum_temp / period, 1))
                result["humidity"].append(round(sum_humidity / period, 1))
                result["moisture"].append(round(sum_moisture / period, 1))
                result["luminosity"].append(round(sum_luminosity / period, 1))
                result["label"].append(label)

                sum_temp = 0
                sum_humidity = 0
                sum_moisture = 0
                sum_luminosity = 0

        return result


def save_sensors_data(t: float, h: int, m: int, l: int):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO data (temp, humidity, moisture, luminosity) "
            "VALUES (?, ?, ?, ?)",
            (t, h, m, l),
        )
        connection.commit()
