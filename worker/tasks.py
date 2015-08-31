from datetime import timedelta
from app import app, db
from models import Record
from utils import get_onewire_value
from celery.decorators import periodic_task


@periodic_task(run_every=timedelta(seconds=app.config['WORKER_FREQUENCY']))
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
