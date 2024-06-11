
import datetime

G_PROPERTIES = {
    'ghost': '=4Wauc3dvJ3Z',
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




