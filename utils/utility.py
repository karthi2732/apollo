
import sys
from plyer import notification


CURSOR_UP_ONE               = '\x1b[1A' 
ERASE_LINE                  = '\x1b[2K' 


def clear_line():
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE) 

def trigger_notification(notification_title, notification_msg):
    notification.notify( title = f'{notification_title}', message = f'{notification_msg}', timeout = 2)