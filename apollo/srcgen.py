
from hermes.crud import * 
from hermes.entities import GStk
from gapis.apis import *
from utils.utility import *


def persist_page_data(records):

    search_ids = [record.get('searchId') for record in records]
    existing_stks = get_stk_by_ids(search_ids)

    stks_page_dict = {}
    
    for stk in existing_stks:
        stks_page_dict.update({stk.search_id: stk})

    for search_id in search_ids:
        if(stks_page_dict.get(search_id) is None):
            stk = GStk()
            stk.search_id = search_id
            stks_page_dict[stk.search_id] = stk

    responses = []

    for search_id in search_ids:
        responses.append(get_thread_pool().submit(get_stk_by_search_id, search_id=search_id, raise_exception=False))
    
    concurrent.futures.wait(responses)

    for i in range(len(responses)): 
        
        response = responses[i].result()
        search_id = search_ids[i]   

        if(response==None):
            print(f'no response found for API request {search_id}')
            stks_page_dict.pop(search_id)
            continue

        stk = stks_page_dict.get(search_id)
        
        if(response.get('header').get('nseScriptCode') is not None):
            stk.exchange = 'NSE'
            stk.code = response.get('header').get('nseScriptCode')
        elif(response.get('header').get('bseScriptCode') is not None):
            stk.exchange = 'BSE'
            stk.code = response.get('header').get('bseScriptCode')
        else:
            print('Unknow Exchange Found: \n', response.get('header'), '\n')
            stks_page_dict.pop(search_id)

    save_stks(list(stks_page_dict.values()))


def reset_tradability(stks):
    stk_week_chart_responses = []
    
    for stk in stks:
        stk_week_chart_responses.append(get_thread_pool().submit(get_stk_chart_data, exchange=stk.exchange, code=stk.code, fetch_freq='weekly', raise_exception=False))

    concurrent.futures.wait(stk_week_chart_responses)

    for i in range(len(stk_week_chart_responses)):

        stk_week_candle_response = stk_week_chart_responses[i].result()
        
        if(stk_week_candle_response is None):
            print(f'Week Chart Not Found {stks[i].search_id}')
            continue

        stk_week_candle = stk_week_candle_response.get('candles')
        
        tradable = (len(stk_week_candle)>=300 and longest_unchanged_price_subset_length(stk_week_candle)<24)

        if(stks[i].tradable is True and tradable is False):
            print(f'Tradable exhibited Non Tradable property {stks[i].search_id}')
        
        stks[i].tradable = tradable
    
    save_stks(stks)


if(__name__=='__main__'):

    ### Populate basic data of All Stk in DB
    process_all_gstks(persist_page_data, raise_exception=False)
    
    ### Update tradability of Stks as per week tradability
    process_all_db_stks(reset_tradability)

    shutdown_thread_pool()

