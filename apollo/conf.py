import os

from pytz import timezone


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "deploy", "db.sqlite")

PERIODS = {"live": 1, "hourly": 12, "daily": 12 * 24, "weekly": 12 * 24 * 7}
DT_FORMAT = "%Y-%m-%d %H:%M:%S"
LOCAL_TZ = timezone("Europe/Minsk")

SPI_PORT = 0
SPI_DEVICE = 0

DHT22_CHANNEL = 25

SMS_CHANNEL = 1
SMS_LOW = 1.12148
SMS_HIGH = 2.78438

LMS_CHANNEL = 0
LMS_LOW = 0.07077
LMS_HIGH = 2.96163

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)-8s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "filesystem": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            # "filename": "/home/pi/apollo/log/apollo.log",
            "filename": "/home/manti/www/manti/apollo/apollo.log",
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {"handlers": ["console", "filesystem"], "level": "DEBUG", "propagate": True}
    },
}
