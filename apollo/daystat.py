

from hermes.crud import * 
from hermes.entities import GStk
from gapis.apis import *
from utils.utility import *



def populate_day_change(stks):

    stk_latest_data_responses = []
    search_ids = []

    for stk in stks:

        if(stk.tradable):
            search_ids.append(stk.search_id)
            stk_latest_data_responses.append(get_thread_pool().submit(get_live_price, exchange = stk.exchange, code=stk.code, raise_exception=False))

    stk_stats = get_stk_stats_by_ids(search_ids)

    stk_stats_dict = {}

    for stk_stat in stk_stats:
        stk_stats_dict.update({stk_stat.search_id: stk_stat})

    concurrent.futures.wait(stk_latest_data_responses)

    for i in range(len(stk_latest_data_responses)):
        
        if(stk_latest_data_responses[i] is not None and stk_latest_data_responses[i].result() is not None):
            
            if(stk_stats_dict.get(search_ids[i]) is None):
                stk_day_stat = GStkDayStat()
            else:
                stk_day_stat = stk_stats_dict.get(search_ids[i])

            stk_day_stat.search_id          = search_ids[i]
            stk_day_stat.open_price         = stk_latest_data_responses[i].result().get('open')
            stk_day_stat.live_price         = stk_latest_data_responses[i].result().get('ltp')
            stk_day_stat.day_change         = stk_latest_data_responses[i].result().get('dayChange')
            stk_day_stat.day_change_perc    = stk_latest_data_responses[i].result().get('dayChangePerc')
            
            stk_stats_dict.update({stk_day_stat.search_id: stk_day_stat})


    if(len(stk_stats_dict.values())>0):
        save_stk_stats(list(stk_stats_dict.values()))


if(__name__=='__main__'):
    process_all_db_stks(populate_day_change, batch_size=50)

