from datetime import datetime
from tinydb import TinyDB, where

from core.conf import settings
from core.utils import get_logger

logger = get_logger()


class Item:

    fields = ('id', 'temp', 'humidity', 'datetime',)

    def __init__(self, data):
        self.data = {
            'datetime': datetime.utcnow().strftime(settings['dt_format'])
        }
        try:
            if 'id' not in data:
                raise Exception('Item id can not be Null')
            if 'temp' not in data:
                raise Exception('Item temp can not be Null')
            if 'humidity' not in data:
                raise Exception('Item humidity can not be Null')

            self.data['id'] = data['id']
            self.data['temp'] = float(data['temp'])
            self.data['humidity'] = float(data['humidity'])
        except Exception as e:
            logger.error(e)
            raise e

        try:

            if 'datetime' in data:
                date_time = datetime.strptime(data['datetime'], settings['dt_format'])
                if date_time:
                    self.data['datetime'] = date_time.strftime(settings['dt_format'])
        except Exception as e:
            logger.info(e)

    @property
    def __dict__(self):
        return self.data


class DB:

    _debug_data = {
        'Guest Room': {'temp': 22.5, 'humidity': 62.2},
        'Work Room': {'temp': 20.8, 'humidity': 55.7},
        'Bedroom': {'temp': 21.1, 'humidity': 57.1},
        'Bathroom': {'temp': 25.1, 'humidity': 94.9},
        '2nd Floor': {'temp': 23.7, 'humidity': 69.3},
    }

    def __init__(self):
        self.db = TinyDB(settings['db_path'])

    def add(self, data):
        item = Item(data)
        self.db.insert(item.__dict__)

    def get(self):
        if settings['debug']:
            return self._debug_data

        result = {}
        for sensor in settings['sensors']:
            value = self.db.search(where('id') == sensor['mac'])[-1]
            result[sensor['name']] = {'temp': value['temp'],
                                      'humidity': value['humidity'],
                                      'datetime': value['datetime']}
        return result
