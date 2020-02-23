import os
import sqlite3
from datetime import datetime

from flask import request
from pytz import timezone, utc

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db.sqlite")
PERIODS = {"live": 1, "hourly": 12, "daily": 12 * 24, "weekly": 12 * 24 * 7}
DT_FORMAT = "%Y-%m-%d %H:%M:%S"
LOCAL_TZ = timezone("Europe/Minsk")


def get_data() -> tuple:
    _type = request.args.get("type", "absolute")
    limit = request.args.get("limit", 10)
    group = request.args.get("group", "hourly")

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

        return result, {"type": _type, "limit": limit, "group": group}


def save_data(t: float, h: int, m: int, l: int):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO data (temp, humidity, moisture, luminosity) "
            "VALUES (?, ?, ?, ?)",
            (t, h, m, l),
        )
        connection.commit()
