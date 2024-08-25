from urllib.parse import quote
import requests, datetime, time, conf
import conf.config, conf.util


################ EXECUTES API CALLS WITH RETRIES ############################

def call(url, method, headers, payload, retry_count, raise_exception):
    
    api_call_count  = retry_count + 1
    api_response    = None

    while (api_call_count>0):

        api_call_count-= 1

        api_response = requests.request(url=url, method=method, headers=headers, json=payload)

        if(api_response.status_code<300):
            break    

        print(f'__API_CALL_FAILED__: {url} STATUS: {api_response.status_code}')
        time.sleep(conf.config.RETRY_FREQUENCY_IN_SECONDS)

    if(api_response.status_code>299):
        print(f'__RETRY_EXHAUSTED__ __API_CALL_FAILED__: {url} STATUS: {api_response.status_code}')
        if(raise_exception):
            raise Exception()
        return None

    return api_response.json()

######################## RETURNS HEADER DICT ###############################

def get_auth_headers():
    return { 'Authorization': f'Bearer {conf.config.G_PROPERTIES.get("ubt")}', 'x-user-campaign': f'Bearer {conf.config.G_PROPERTIES.get("uct")}' }

######################## RETURNS LIVEPRICE DICT ############################

def get_live_price(exchange, code, retry_count=conf.config.DEFAULT_RETRY_COUNT, raise_exception = True):
    url = f'https://{conf.config.G_PROPERTIES.get("ghost")}/v1/api/stocks_data/v1/tr_live_prices/exchange/{exchange}/segment/CASH/{quote(code)}/latest'
    live_price_data = call(url, 'GET', None, None, retry_count, raise_exception)
    return live_price_data

######################## RETURNS STK CHART CANDLES #########################

def get_stk_chart_data(exchange, code, interval_min=1, fetch_freq='daily', retry_count=conf.config.DEFAULT_RETRY_COUNT, raise_exception=True):
    url = f'https://{conf.config.G_PROPERTIES.get("ghost")}/v1/api/charting_service/v2/chart/exchange/{exchange}/segment/CASH/{quote(code)}/{fetch_freq}?intervalInMinutes={interval_min}&minimal=true'
    stock_chart_data = call(url, 'GET', None, None, retry_count, raise_exception)
    stock_chart_data['exchange'] = exchange
    stock_chart_data['code'] = code
    return stock_chart_data

####################### GET STK BY SEARCH ID ###############################

def get_stk_by_search_id(search_id, retry_count=conf.config.DEFAULT_RETRY_COUNT, raise_exception = True):
    url = f'https://{conf.config.G_PROPERTIES.get("ghost")}/v1/api/stocks_data/v1/company/search_id/{search_id}?page=0&size=10'
    stock_data = call(url, 'GET', None, None, retry_count, raise_exception)
    return stock_data

######################## LIST ALL STKS API #################################

def get_all_stks_data(page = 0, size = 25, sort_type = 'ASC', sort_by = 'NA', stock_indices = [], stock_industry = [], retry_count = conf.config.DEFAULT_RETRY_COUNT, raise_exception = True): 
    
    get_all_stocks_req = {}
    get_all_stocks_req['listFilters'] = {}
    get_all_stocks_req['page'] = page
    get_all_stocks_req['size'] = size
    get_all_stocks_req['sortType'] = sort_type
    get_all_stocks_req['sortBy'] = sort_by
    get_all_stocks_req['listFilters']['INDEX'] = stock_indices
    get_all_stocks_req['listFilters']['INDUSTRY'] = stock_industry

    url = f'https://{conf.config.G_PROPERTIES.get("ghost")}/v1/api/stocks_data/v1/all_stocks'

    paginated_stocks = call(url, 'POST', None, get_all_stocks_req, retry_count, raise_exception)

    return paginated_stocks

######################### LIST CURRENT HOLDING STKS #########################

def get_current_holding_stks(retry_count=conf.config.DEFAULT_RETRY_COUNT, raise_exception=True):
    url = f'https://{conf.config.G_PROPERTIES.get("ghost")}/v1/api/stocks_router/v6/dashboard?ts={datetime.datetime.now()}&source=other'
    req_headers = get_auth_headers()
    current_holding_response = call(url, 'GET', req_headers, None, retry_count, raise_exception)
    return current_holding_response

#############################################################################


