
import datetime

NOTIFICATION_ENABLED            = True
NOTIFICATION_INTERVAL_SECONDS   = 5
NOTIFICATION_TIME_DELTA         = datetime.timedelta(seconds=NOTIFICATION_INTERVAL_SECONDS)
LAST_NOTIFIED_TIME_STAMP        = datetime.datetime.now() - NOTIFICATION_TIME_DELTA

PROBE_FREQUENCY_IN_SECONDS      = 5
RETRY_FREQUENCY_IN_SECONDS      = 5

DEFAULT_ITERATION_LIMIT         = 500
DEFAULT_API_PAGE_SIZE           = 25
DEFAULT_DB_BATCH_SIZE           = 25
DEFAULT_RETRY_COUNT             = 3


DB_USER_NAME                    = 'root'
DB_PASSWORD                     = ''
DB_HOST                         = '127.0.0.1'
DB_PORT                         = '3306'
DB_NAME                         = 'apollo'

"""
Overriding Configs for above mentioned Configs are specified in `overrides.py`

"""
from .overrides import *


DB_URL          = f'mysql+mysqlconnector://{DB_USER_NAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'


