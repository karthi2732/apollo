import datetime, json, time
from conf.util import decode_prop
from utils.utility import clear_line, trigger_notification
from gapis.apis import *


GHOST = conf.util.decode_prop(conf.config.G_PROPERTIES.get('ghost'))


def get_probe_data_list():
    probe_data_list = json.load(open('conf/config.json'))
    for probe_data in probe_data_list:
        probe_data.update( { 'lastNotifiedTimestamp': (conf.config.LAST_NOTIFIED_TIME_STAMP-conf.config.NOTIFICATION_TIME_DELTA) } )
    return probe_data_list


def shoot(targeted_stks):
    while(True):
        for stk in targeted_stks:
            print(f'{stk.get("symbol")} probing... ')
            live_data = get_live_price(stk.get('stockExchange'), stk.get('symbol'), 3, False)
            clear_line()

            if(live_data.get('ltp')>stk.get('sellBoundary') and stk.get('sellBoundaryNotificationEnabled') and datetime.datetime.now()>(stk.get('lastNotifiedTimestamp')+conf.config.NOTIFICATION_TIME_DELTA)):
                print(f'https://{GHOST}/stocks/{stk.get("searchId")}')
                trigger_notification(stk.get('symbol'), live_data.get('ltp'))
                stk.update({ 'lastNotifiedTimestamp': datetime.datetime.now() })
            
            elif(live_data.get('ltp')<stk.get('buyBoundary') and stk.get('buyBoundaryNotificationEnabled') and datetime.datetime.now()>(stk.get('lastNotifiedTimestamp')+conf.config.NOTIFICATION_TIME_DELTA)):
                print(f'https://{GHOST}/stocks/{stk.get("searchId")}')
                trigger_notification(stk.get('symbol'), live_data.get('ltp'))
                stk.update({ 'lastNotifiedTimestamp': datetime.datetime.now() })
        
        print('sleeping...')
        clear_line()

        time.sleep(conf.config.PROBE_FREQUENCY_IN_SECONDS)


if(__name__=='__main__'):

    shoot(get_probe_data_list())


