import RPi.GPIO as GPIO
import time


def buzzer_short_low(id):
    buzzer = GPIO.PWM(id, 400)
    buzzer.start()
    time.sleep(0.1)
    buzzer.stop()

def buzzer_double_short_low(id):
    buzzer_short_low(id)
    time.sleep(5)
    buzzer_short_low(id)

def buzzer_long_low(id):
    buzzer = GPIO.PWM(id, 400)
    buzzer.start()
    time.sleep(0.5)
    buzzer.stop()

def buzzer_double_long_low(id):
    buzzer_long_low(id)
    time.sleep(1)
    buzzer_long_low(id)

def buzzer_alert_long_low(id):
    for i in range(5):
        buzzer_long_low(id)
        time.sleep(1)

