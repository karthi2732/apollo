
import datetime

G_PROPERTIES = {
    'ghost': '',
    'ubt': '',
    'uct': ''
}

NOTIFICATION_ENABLED            = True
NOTIFICATION_INTERVAL_SECONDS   = 5
NOTIFICATION_TIME_DELTA         = datetime.timedelta(seconds=NOTIFICATION_INTERVAL_SECONDS)
LAST_NOTIFIED_TIME_STAMP        = datetime.datetime.now() - NOTIFICATION_TIME_DELTA

PROBE_FREQUENCY_IN_SECONDS      = 5
RETRY_FREQUENCY_IN_SECONDS      = 5

DEFAULT_ITERATION_LIMIT         = 500
DEFAULT_BATCH_SIZE              = 25
DEFAULT_RETRY_COUNT             = 3


DB_USER_NAME                    = 'root'
DB_PASSWORD                     = None
DB_HOST                         = '127.0.0.1'
DB_PORT                         = 3306
DATABASE                        = ''

################## CREATE A NEW config_local.py IN THE SAME PYTHON PACKAGE #########
################## ADD OVERRIDING PROPERTIES IN FOLLOWING MODULE ###################

from conf.config_local import *

