import random
import logging
from config import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Record
from utils import get_onewire_value


# Setup logging
logging.basicConfig(level = logging.ERROR, filename = LOG_FILE)

# Setup database engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
session = sessionmaker(bind=engine)


if __name__ == "__main__":
    try:
        if IS_RPI:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(TERM_INPUT, GPIO.IN)
            data = {
                'term_01' : get_onewire_value(TERM_01),
                'term_02' : get_onewire_value(TERM_02)
            }
        else:
            data = {
                'term_01' : random.uniform(21.5, 79.1),
                'term_02' : random.uniform(55.1, 92.5)
            }

        # Store data into DB
        r = Record(**data)
        session.add(r)
        session.commit()
        logging.info('Record processed')
    except Exception as e:
        logging.error(e.message)