from datetime import datetime
from operator import itemgetter
from tinydb import TinyDB, where

from core.conf import settings
from core.utils import get_logger

logger = get_logger()


class Item:

    fields = ('mac', 'temp', 'humidity', 'datetime',)

    def __init__(self, data):
        self.data = {
            'datetime': datetime.utcnow().strftime(settings['dt_format'])
        }
        try:
            if 'mac' not in data:
                raise Exception('Item mac can not be Null')
            if 'temp' not in data:
                raise Exception('Item temp can not be Null')
            if 'humidity' not in data:
                raise Exception('Item humidity can not be Null')

            self.data['mac'] = data['mac']
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

    def __init__(self):
        self.db = TinyDB(settings['db_path'])

    def add(self, data):
        item = Item(data)
        self.db.insert(item.__dict__)

    def get(self):
        result = {}
        for mac, name in settings['sensors'].items():
            sensor_data = self.db.search(where('mac') == mac)
            if sensor_data:
                value = sorted(sensor_data, key=itemgetter('datetime'), reverse=True)[0]
                result[name] = {
                    'temp': value['temp'],
                    'humidity': value['humidity'],
                    'datetime': value['datetime']
                }
        return result

    def search(self, filters):
        result = []
        sensor_data = self.db.search(where('mac') == filters['mac'])
        if sensor_data:
            for item in sorted(sensor_data, key=itemgetter('datetime'), reverse=True):
                if filters['start_date'] <= item['datetime'] <= filters['end_date']:
                    result.append({
                        'temp': item['temp'],
                        'humidity': item['humidity'],
                        'datetime': item['datetime']
                    })
        return result
