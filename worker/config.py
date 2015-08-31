import os
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
HOST = '0.0.0.0'

LOG_FILE = 'app.log'
WORKER_FREQUENCY = 5

TERM_INPUT = 7
TERM_01 = '000007173569'
TERM_02 = '000007177269'

SQLALCHEMY_DATABASE_URI = 'mysql://pibot:P1B0t@192.168.1.2/pibot'
SQLALCHEMY_MIGRATE_REPO = os.path.join(ROOT_PATH, '../database')

BROKER_BACKEND = "sqlakombu.transport.Transport"
BROKER_HOST = 'mysql://pibot:P1B0t@192.168.1.2/pibot'
CELERY_RESULT_DBURI = 'mysql://pibot:P1B0t@192.168.1.2/pibot'
