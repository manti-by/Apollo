import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "deploy", "db.sqlite")

SPI_PORT = 0
SPI_DEVICE = 0

DHT22_CHANNEL = 25

SMS_CHANNEL = 1
SMS_LOW = 1.12148
SMS_HIGH = 2.78438

LMS_CHANNEL = 0
LMS_LOW = 0.07077
LMS_HIGH = 2.96163
