import os
import sqlite3

from apollo.conf import DB_PATH


def get_currency_data() -> dict:
    with sqlite3.connect(DB_PATH) as session:
        session.row_factory = sqlite3.Row
        cursor = session.cursor()
        cursor.execute(
            "SELECT usd_buy, usd_sell, eur_buy, eur_sell, rur_buy, rur_sell, datetime "
            "FROM currency ORDER BY datetime DESC",
        )
        session.commit()
        return dict(cursor.fetchone())


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
