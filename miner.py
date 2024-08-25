
from gapis.apis import get_all_stks_data, get_stk_chart_data, get_live_price
from db.odin import *
import time, conf.config, math, concurrent.futures, json, sys
from conf.util import *


GLOBAL_THREAD_POOL  = None


######################### INITIALISE THREAD POOL ##############################

def get_thread_pool():
    global GLOBAL_THREAD_POOL
    if(GLOBAL_THREAD_POOL is None):
        GLOBAL_THREAD_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    return GLOBAL_THREAD_POOL


######################### SHUTDOWN THREAD POOL ################################

def shutdown_thread_pool():
    global GLOBAL_THREAD_POOL
    if(GLOBAL_THREAD_POOL is not None):
        GLOBAL_THREAD_POOL.shutdown(wait=True)

######################### ITERATE STKS FROM SERVER #############################

def analyse_all_gstks(analyse_func, analysis_output, page_number = 0, page_size = 25, iteration_threshold = conf.config.DEFAULT_ITERATION_LIMIT):
    
    if(iteration_threshold<=0):
        iteration_threshold = conf.config.DEFAULT_ITERATION_LIMIT

    has_more_stocks = True

    while(iteration_threshold>0 and has_more_stocks):

        print(f'PageNumber: {page_number} PageSize: {page_size} ThresholdCount: {iteration_threshold} HasMoreStocks: {has_more_stocks}')

        paginated_stock_list = get_all_stks_data(page=page_number, size=page_size)
        analyse_func(paginated_stock_list['records'], analysis_output)

        has_more_stocks = ( paginated_stock_list['totalRecords'] - ((page_number+1)*page_size) ) > 0
        iteration_threshold-= 1
        page_number+= 1


######################### ITERATE STKS FROM DB #############################

def analyse_all_db_stks(analyse_func, analysis_output, page_number = 0, page_size = 25, iteration_threshold = None):

    if (iteration_threshold is None):
        iteration_threshold = math.ceil(get_stk_cnt()/page_size)

    while(iteration_threshold>0):
        
        offset = page_number*page_size
        limit = offset+page_size
    
        print(f'Offset: {offset} LimitTill: {limit} ThresholdCount: {iteration_threshold}')

        ids = get_search_id_from_db(page_number*page_size, page_size)
        stk_data_list = get_stk_details(ids)

        analyse_func(stk_data_list, analysis_output)

        iteration_threshold-= 1
        page_number+= 1


######################### EXTRACT LIVE DATA ################################

def populate_changers_dict_from_list_stks(records_list, changers_list):
    for record in records_list:
        stk_change_data = {}
        stk_change_data['search_id'] = record.get('searchId')
        stk_change_data['symbol'] = record.get('livePriceDto').get('symbol')
        stk_change_data['open_price'] = record.get('livePriceDto').get('open')
        stk_change_data['day_change'] = record.get('livePriceDto').get('dayChange')
        stk_change_data['day_change_perc'] = record.get('livePriceDto').get('dayChangePerc')
        if(is_stk_tradable(record.get('searchId'))):
            ydate = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            stk_change_data['search_string'] = 'news on ' + (stk_change_data['search_id']).replace('-', ' ') + ' after:' + ydate
            changers_list.append(stk_change_data)


######################### ITERATE STKS FROM DB #############################

def list_day_changers():
    open_connection()
    changers = []
    analyse_all_gstks(analyse_func=populate_changers_dict_from_list_stks, analysis_output=changers)
    
    sort_dict(changers, 'day_change_perc', 0, len(changers)-1)
    
    print()
    printed_search_ids = set()
    for changer in changers:
        if(not printed_search_ids.__contains__(changer.get('search_id'))):
            printed_search_ids.add(changer.get('search_id'))
            print(json.dumps(changer,indent=4))
    close_connection()


######################### POPULATE STKS DATA IN DB #########################

def extract_and_upsert_stk(record_list, analysis_output):
    
    for record in record_list:

        if(record.get("marketCap")==0 or record.get("growwContractId")==None or record.get("isin")==None):
            continue
        
        if(record.get("yearlyHighPrice")==None or record.get("yearlyLowPrice")==None or record.get("livePriceDto")==None or record.get("livePriceDto").get("ltp")==None or record.get("yearlyLowPrice")==0):
            continue
    
        if(record.get("nseScriptCode")!=None):
            exchange = 'NSE'
            code = record.get("nseScriptCode")
        elif(record.get("bseScriptCode")!=None):
            exchange = 'BSE'
            code = record.get("bseScriptCode")
        else:
            print(record)
            continue
        
        stk_data = { 'search_id': record.get("searchId"), 'code': code, 'exchange': exchange, 'g_contract_id': record.get("growwContractId"), 'isin': record.get("isin") }

        upsert_data(stk_data)


######################### POPULATE STKS DATA IN DB #########################

def populate_stks_in_db():
    open_connection()
    analyse_all_gstks(analyse_func=extract_and_upsert_stk, analysis_output=None)
    close_connection()


######################### POPULATE STKS DATA IN DB #########################

def analyse_and_update_trability(record_list, analysis_output):
    stk_chart_list = []
    for record in record_list:
        stk_chart = get_thread_pool().submit(get_stk_chart_data, exchange=record.get('exchange'), code=record.get('code'), fetch_freq='weekly')
        stk_chart_list.append(stk_chart)
    
    concurrent.futures.wait(stk_chart_list)
    tradable_stk_id_list = []
    non_tradable_stk_id_list = []

    for i in range(len(stk_chart_list)):
        stk_candle = stk_chart_list[i].result().get('candles')
        # If a stk candle's range is less than 300 per week or the stk value is not changed for 2 hours continiously, it is not suitable for trades
        if(len(stk_candle)<300 or longest_unchanged_price_subset_length(stk_candle)>=24):
            non_tradable_stk_id_list.append(record_list[i].get('search_id'))
        else:
            tradable_stk_id_list.append(record_list[i].get('search_id'))

    update_tradability(tradable_stk_id_list, 1)
    update_tradability(non_tradable_stk_id_list, 0)    


######################### POPULATE STKS DATA IN DB #########################

def update_stk_tradability():
    open_connection()
    analyse_all_db_stks(analyse_func=analyse_and_update_trability, analysis_output=None)
    shutdown_thread_pool()
    close_connection()


######################### DELVE STKS DATA FOR MOVERS #######################

def delve_market_bulls(record_list, analysis_output):
    stk_chart_list = []
    for record in record_list:
        if(record.get('tradable')):
            stk_chart = get_thread_pool().submit(get_stk_chart_data, exchange=record.get('exchange'), code=record.get('code'), fetch_freq='weekly')
            stk_chart_list.append(stk_chart)
    
    concurrent.futures.wait(stk_chart_list)

    for i in range(len(stk_chart_list)):
        
        stk_candle = stk_chart_list[i].result().get('candles')
        bull_cnt = 0
        date = datetime.datetime.fromtimestamp(stk_candle[0][0]).date()
        price = stk_candle[0][1]
        
        for candle in stk_candle[1:]:
            
            if(date!=datetime.datetime.fromtimestamp(candle[0]).date()):
                
                if(candle[1]-price>0):
                    bull_cnt+= 1
                
                date = datetime.datetime.fromtimestamp(candle[0]).date()
                price = candle[1]

        if(bull_cnt>=3):
            analysis_output.append(stk_chart_list[i].result().get('code'))
        # analysis_output.append(f"{stk_chart_list[i].result().get('code')} {bull_cnt}")

def delve_market_bears(record_list, analysis_output):
    stk_chart_list = []
    for record in record_list:
        if(record.get('tradable')):
            stk_chart = get_thread_pool().submit(get_stk_chart_data, exchange=record.get('exchange'), code=record.get('code'), fetch_freq='weekly')
            stk_chart_list.append(stk_chart)
    
    concurrent.futures.wait(stk_chart_list)

    for i in range(len(stk_chart_list)):
        
        stk_candle = stk_chart_list[i].result().get('candles')
        bear_cnt = 0
        date = datetime.datetime.fromtimestamp(stk_candle[0][0]).date()
        price = stk_candle[0][1]
        
        for candle in stk_candle[1:]:
            
            if(date!=datetime.datetime.fromtimestamp(candle[0]).date()):
                
                if(candle[1]-price<0):
                    bull_cnt+= 1
                
                date = datetime.datetime.fromtimestamp(candle[0]).date()
                price = candle[1]

        if(bear_cnt>=3):
            analysis_output.append(stk_chart_list[i].result().get('code'))


######################### POPULATE STKS DATA IN DB #########################

def movers(movement):
    open_connection()
    movers = []
    if(movement=='bull'):
        analyse_all_db_stks(analyse_func=delve_market_bulls, analysis_output=movers)
    elif(movement=='bear'):
        analyse_all_db_stks(analyse_func=delve_market_bears, analysis_output=movers)
    for mover in movers:
        print(mover)
    shutdown_thread_pool()
    close_connection()


############################################################################

if(__name__=='__main__'):

    if(len(sys.argv)<2):

        print('Enter Action Number of Miner: ')
        print('1. LIST_DAY_CHANGERS')
        print('2. POPULATE_STK_IN_DB')
        print('3. UPDATE_TRADABILITY')
        print('4. BULL_RUNNERS')
        print('5. BEAR_RUNNERS')
        print('6. GET_PERCENTILE_BREACHERS')
        
        print()
        action = int(input())

    # action = 0
    print()

    start_time = time.time()

    if(action==1):
        list_day_changers()
    elif(action==2):
        populate_stks_in_db()
    elif(action==3):
        update_stk_tradability()
    elif(action==4):
        movers('bull')
    elif(action==5):
        movers('bear')

    end_time = time.time()
    print(f'\nMiner Execution Time = {round(end_time-start_time)}s\n')


