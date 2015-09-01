DEBUG = True
HOST = '0.0.0.0'

LOG_FILE = 'app.log'
WORKER_FREQUENCY = 5

TERM_INPUT = 7
TERM_01 = '000007173569'
TERM_02 = '000007177269'

SQLALCHEMY_DATABASE_URI = 'mysql://pibot:P1B0t@192.168.1.2/pibot'

BROKER_BACKEND = "sqlakombu.transport.Transport"
BROKER_URL = 'sqla+mysql://pibot:P1B0t@192.168.1.2/pibot'
BACKEND_URL = 'sqla+mysql://pibot:P1B0t@192.168.1.2/pibot'

from locals import *