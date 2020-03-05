import requests

import xml.etree.ElementTree as ET

from apollo.database.currency import save_currency_data


if __name__ == "__main__":
    response = requests.get('https://www.mtbank.by/currxml.php?ver=2')

    if response.status_code == 200:
        usd_buy = 0
        usd_sell = 0
        eur_buy = 0
        eur_sell = 0
        rur_buy = 0
        rur_sell = 0
        for child in ET.fromstring(response.content):
            if child.attrib.get('id') == '168,768,968,868':
                for currency in child.findall('currency'):
                    if currency.find('code').text == 'BYN' and currency.find('codeTo').text == 'USD':
                        usd_buy = float(currency.find('purchase').text)
                        usd_sell = float(currency.find('sale').text)
                    if currency.find('code').text == 'BYN' and currency.find('codeTo').text == 'EUR':
                        eur_buy = float(currency.find('purchase').text)
                        eur_sell = float(currency.find('sale').text)
                    if currency.find('code').text == 'BYN' and currency.find('codeTo').text == 'RUB':
                        rur_buy = float(currency.find('purchase').text)
                        rur_sell = float(currency.find('sale').text)

        save_currency_data(usd_buy, usd_sell, eur_buy, eur_sell, rur_buy, rur_sell)
        print(
            "Currency: {:0.2f}/{:0.2f} USD, {:0.2f}/{:0.2f} EUR, {:0.2f}/{:0.2f} RUR".format(
                usd_buy, usd_sell, eur_buy, eur_sell, rur_buy, rur_sell
            )
        )
    else:
        print("Error: {}", response.errors)
