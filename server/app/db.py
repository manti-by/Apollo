from datetime import datetime
from tinydb import TinyDB, Query, where

from .conf import settings
from .utils import get_logger

logger = get_logger()


class Item(Query):

    fields = ('id', 'temp', 'humidity', 'datetime',)

    def __init__(self, data: dict):
        self.data = {}
        try:
            if 'id' not in data:
                raise Exception('Item id can not be Null')
            if 'temp' not in data:
                raise Exception('Item temp can not be Null')
            if 'humidity' not in data:
                raise Exception('Item humidity can not be Null')

            self.data['id'] = int(data['id'])
            self.data['temp'] = float(data['temp'])
            self.data['humidity'] = float(data['humidity'])
        except Exception as e:
            logger.error(e)
            raise e

        try:
            if 'datetime' in data:
                dt = datetime.strptime(data['datetime'], settings['dt_format'])
                if dt:
                    self.data['datetime'] = dt.strftime(settings['dt_format'])
                    del data['datetime']
        except Exception as e:
            self.data['datetime'] = datetime.utcnow().strftime(settings['dt_format'])
            logger.info(e)

    @property
    def __dict__(self) -> dict:
        return self.data


class DB:

    def __init__(self):
        self.db = TinyDB(settings['db_path'])

    def add(self, data: dict):
        item = Item(data)
        self.db.insert(item.__dict__)

    def get(self) -> dict:
        result = {}
        for sensor in settings['sensors']:
            value = self.db.search(where('id') == sensor['mac'])[0]
            result[sensor['mac']] = {'temp': value['temp'],
                                     'humidity': value['humidity'],
                                     'datetime': value['datetime']}
        return result
