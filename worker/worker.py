import logging
import RPi.GPIO as GPIO

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import *
from models import Record
from utils import check_rules, draw_display, read_onewire_channel, read_spi_channel


# Setup logging
logging.basicConfig(level = logging.ERROR, filename = LOG_FILE)

# Setup database engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TERM_INPUT, GPIO.IN)
        GPIO.setup(BUZZER_OUTPUT, GPIO.OUT)

        # Compile data
        data = {
            'term_01'       : read_onewire_channel(TERM_01),
            'term_02'       : read_onewire_channel(TERM_02),
            'term_03'       : read_onewire_channel(TERM_03),
            'term_04'       : read_onewire_channel(TERM_04),
            'term_05'       : read_onewire_channel(TERM_05),
            'water_sensor'  : read_spi_channel(MOISTURE_INPUT),
            'timestamp'     : datetime.now()
        }

        # Store data into DB
        r = Record(**data)
        session.add(r)
        session.commit()

        # Check rules and draw data
        check_rules(data, BUZZER_OUTPUT)
        draw_display(data, DISPLAY_OUTPUT)

        GPIO.cleanup()
        logging.info('Record processed')
    except Exception as e:
        logging.error(e.message)