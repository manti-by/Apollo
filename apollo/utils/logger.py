import logging.config

from apollo.conf import LOGGING


def init_logger():
    logging.config.dictConfig(LOGGING)
