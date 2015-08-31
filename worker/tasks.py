from app import db
from models import Record
from utils import get_onewire_value
from celery.decorators import periodic_task


@periodic_task(run_every=timedelta(seconds=1))
def get_sensor_data():
    try:
        data = {
            'term_01' : get_onewire_value(app.config['TERM_01']),
            'term_02' : get_onewire_value(app.config['TERM_02'])
        }
        r = Record(**data)
        db.session.add(r)
        db.session.commit()
    except Exception as e:
        app.logger.error(e.message)
