import requests

import xml.etree.ElementTree as ET

from apollo.database.weather import save_weather_data


if __name__ == "__main__":
    response = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?q=Minsk,'
        'by&units=metric&appid=aec9289a4fe49b1bca7296d08c1e170b'
    )

    if response.status_code == 200:
        data = response.json()
        save_weather_data(
            data['main']['temp'], data['main']['pressure'], data['weather'][0]['icon'],
            data['wind']['speed'], data['wind']['deg']
        )
        print(
            "Temp: {:0.2f}*C, pressure {:d}mmHg, icon {:s}, wind speed {:d}m/s, wind direction {:d}*".format(
                data['main']['temp'], data['main']['pressure'], data['weather'][0]['icon'],
                data['wind']['speed'], data['wind']['deg']
            )
        )
    else:
        print("Error: {}", response.errors)
