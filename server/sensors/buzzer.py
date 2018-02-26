import time
import RPi.GPIO as GPIO


def buzzer_short_low(channel_id):
    buzzer = GPIO.PWM(channel_id, 400)
    buzzer.start(20)
    time.sleep(0.1)
    buzzer.stop()


def buzzer_double_short_low(channel_id):
    buzzer_short_low(channel_id)
    time.sleep(5)
    buzzer_short_low(channel_id)


def buzzer_long_low(channel_id):
    buzzer = GPIO.PWM(channel_id, 400)
    buzzer.start(20)
    time.sleep(0.5)
    buzzer.stop()


def buzzer_double_long_low(channel_id):
    buzzer_long_low(channel_id)
    time.sleep(1)
    buzzer_long_low(channel_id)


def buzzer_alert_long_low(channel_id):
    for i in range(5):
        buzzer_long_low(channel_id)
        time.sleep(1)
