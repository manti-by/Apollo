import logging
import logging.config

from .conf import settings

logger = logging.getLogger()


def get_logger():
    logging.basicConfig(level=logging.DEBUG)
    logging.config.dictConfig(settings['logging'])
    return logger
