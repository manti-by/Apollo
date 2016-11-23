import time
import logging
import RPi.GPIO as GPIO

logger = logging.getLogger('sensors')


def buzzer_short_low(channel_id):
    try:
        buzzer = GPIO.PWM(channel_id, 400)
        buzzer.start()
        time.sleep(0.1)
        buzzer.stop()
    except Exception as e:
        logger.error(e.message)
        return -1


def buzzer_double_short_low(channel_id):
    try:
        buzzer_short_low(channel_id)
        time.sleep(5)
        buzzer_short_low(channel_id)
    except Exception as e:
        logger.error(e.message)
        return -1


def buzzer_long_low(channel_id):
    try:
        buzzer = GPIO.PWM(channel_id, 400)
        buzzer.start()
        time.sleep(0.5)
        buzzer.stop()
    except Exception as e:
        logger.error(e.message)
        return -1


def buzzer_double_long_low(channel_id):
    try:
        buzzer_long_low(channel_id)
        time.sleep(1)
        buzzer_long_low(channel_id)
    except Exception as e:
        logger.error(e.message)
        return -1


def buzzer_alert_long_low(channel_id):
    try:
        for i in range(5):
            buzzer_long_low(channel_id)
            time.sleep(1)
    except Exception as e:
        logger.error(e.message)
        return -1
