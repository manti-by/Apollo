import os
import sqlite3

from datetime import datetime
from pytz import utc

from apollo.conf import DB_PATH, PERIODS, DT_FORMAT, LOCAL_TZ


def get_currency_data(limit: int = None, group: str = None) -> dict:
    limit = limit if limit is not None else 10
    group = group if group is not None else "hourly"

    with sqlite3.connect(DB_PATH) as session:
        session.row_factory = sqlite3.Row
        cursor = session.cursor()
        query_limit = PERIODS.get(group, 1) * int(limit)
        cursor.execute(
            "SELECT usd_buy, usd_sell, eur_buy, eur_sell, rur_buy, rur_sell, datetime "
            "FROM currency ORDER BY datetime DESC LIMIT ?",
            (query_limit,),
        )
        session.commit()
        data = cursor.fetchall()[::-1]

        result = {
            "usd_buy": [],
            "usd_sell": [],
            "eur_buy": [],
            "eur_sell": [],
            "rur_buy": [],
            "rur_sell": [],
            "label": [],
        }

        sum_usd_buy = 0
        sum_usd_sell = 0
        sum_eur_sell = 0
        sum_eur_buy = 0
        sum_rur_sell = 0
        sum_rur_buy = 0
        counter = 0

        period = PERIODS.get(group)
        for item in data:
            counter += 1
            sum_usd_buy += item["usd_buy"] or 0
            sum_usd_sell += item["usd_sell"] or 0
            sum_eur_buy += item["eur_buy"] or 0
            sum_eur_sell += item["eur_sell"] or 0
            sum_rur_buy += item["rur_buy"] or 0
            sum_rur_sell += item["rur_sell"] or 0

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
                result["usd_buy"].append(round(sum_usd_buy / period, 2))
                result["usd_sell"].append(round(sum_usd_sell / period, 2))
                result["eur_buy"].append(round(sum_eur_buy / period, 2))
                result["eur_sell"].append(round(sum_eur_sell / period, 2))
                result["rur_buy"].append(round(sum_rur_buy / period, 2))
                result["rur_sell"].append(round(sum_rur_sell / period, 2))
                result["label"].append(label)

                sum_usd_buy = 0
                sum_usd_sell = 0
                sum_eur_sell = 0
                sum_eur_buy = 0
                sum_rur_sell = 0
                sum_rur_buy = 0

        return result


def save_currency_data(
        usd_buy: float, usd_sell: float, eur_buy: float, eur_sell: float, rur_buy: float, rur_sell: float
):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO currency (usd_buy, usd_sell, eur_buy, eur_sell, rur_buy, rur_sell) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (usd_buy, usd_sell, eur_buy, eur_sell, rur_buy, rur_sell),
        )
        connection.commit()
