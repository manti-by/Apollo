import time
import random
import logging
from config import *
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Record
from library.utils import check_rules, draw_display
from library.onewire import get_onewire_value
from library.mcp3008 import get_water_level


# Setup logging
logging.basicConfig(level = logging.ERROR, filename = LOG_FILE)

# Setup database engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    try:
        if IS_RPI:
            import RPi.GPIO as GPIO

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(TERM_INPUT, GPIO.IN)
            GPIO.setup(BUZZER_OUTPUT, GPIO.OUT)

            data = {
                'term_01' : get_onewire_value(TERM_01),
                'term_02' : get_onewire_value(TERM_02),
                'term_03' : get_onewire_value(TERM_03),
                'term_04' : get_onewire_value(TERM_04),
                'term_05' : get_onewire_value(TERM_05),
                'water_sensor': get_water_level(),
            }
        else:
            data = {
                'term_01' : random.uniform(21.5, 79.1),
                'term_02' : random.uniform(55.1, 92.5),
                'term_03' : random.uniform(25.1, 62.5),
                'term_04' : random.uniform(45.1, 110.5),
                'term_05' : random.uniform(55.1, 92.5),
                'water_sensor': random.uniform(0, 1),
            }
        data['timestamp'] = datetime.now()

        # Store data into DB
        r = Record(**data)
        session.add(r)
        session.commit()

        # Check rules and draw data
        check_rules(data, BUZZER_OUTPUT)
        draw_display(data, DISPLAY_RST)

        if IS_RPI:
            GPIO.cleanup()

        logging.info('Record processed')
    except Exception as e:
        logging.error(e.message)