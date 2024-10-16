from urllib.parse import quote
from config.config import *
import requests, datetime, time


"""
Executes the given HTTP request with retires at given sleep interval

"""

def call(url, method, headers, payload, retry_count, raise_exception):
    
    api_call_count  = retry_count + 1
    api_response    = None

    while (api_call_count>0):

        api_call_count-= 1

        api_response = requests.request(url=url, method=method, headers=headers, json=payload)

        if(api_response.status_code<300):
            break 

        print(f'__API_CALL_FAILED__: {url} STATUS: {api_response.status_code}')
        
        if(api_response.status_code==400):
            break 
        
        time.sleep(RETRY_FREQUENCY_IN_SECONDS)

    if(api_response.status_code>299):
        print(f'__RETRY_EXHAUSTED__ __API_CALL_FAILED__: {url} STATUS: {api_response.status_code}')
        if(raise_exception):
            raise Exception()
        return None

    return api_response.json()


"""
Authorization Headers to access g_servers

"""

def get_auth_headers():
    return { 'Authorization': f'Bearer {BEARER_TOKEN}', 'x-user-campaign': f'Bearer {CAMPAIGN_TOKEN}' }


"""
Gets the Live Price Data from Servers

"""

def get_live_price(exchange, code, retry_count=DEFAULT_RETRY_COUNT, raise_exception = True):
    url = f'https://{G_HOST}/v1/api/stocks_data/v1/tr_live_prices/exchange/{exchange}/segment/CASH/{quote(code)}/latest'
    live_price_data = call(url, 'GET', None, None, retry_count, raise_exception)
    return live_price_data


"""
Get the Stk Chart Data from g_server

"""

def get_stk_chart_data(exchange, code, interval_min=1, fetch_freq='daily', retry_count=DEFAULT_RETRY_COUNT, raise_exception=True):
    url = f'https://{G_HOST}/v1/api/charting_service/v2/chart/exchange/{exchange}/segment/CASH/{quote(code)}/{fetch_freq}?intervalInMinutes={interval_min}&minimal=true'
    stock_chart_data = call(url, 'GET', None, None, retry_count, raise_exception)
    stock_chart_data['exchange'] = exchange
    stock_chart_data['code'] = code
    return stock_chart_data


"""
Find the stk using g_search_id and returns the response

"""

def get_stk_by_search_id(search_id, retry_count=DEFAULT_RETRY_COUNT, raise_exception = True):
    url = f'https://{G_HOST}/v1/api/stocks_data/v1/company/search_id/{search_id}?fields=COMPANY_HEADER&page=0&size=10'
    stock_data = call(url, 'GET', None, None, retry_count, raise_exception)
    return stock_data


"""
Iterates the pages and lists the stks

"""

def get_gstk_page(page = 0, size = 25, sort_type = 'ASC', sort_by = 'NA', stock_indices = [], stock_industry = [], retry_count = DEFAULT_RETRY_COUNT, raise_exception = True): 
    
    get_all_stocks_req = {}
    get_all_stocks_req['listFilters'] = {}
    get_all_stocks_req['page'] = page
    get_all_stocks_req['size'] = size
    get_all_stocks_req['sortType'] = sort_type
    get_all_stocks_req['sortBy'] = sort_by
    get_all_stocks_req['listFilters']['INDEX'] = stock_indices
    get_all_stocks_req['listFilters']['INDUSTRY'] = stock_industry

    url = f'https://{G_HOST}/v1/api/stocks_data/v1/all_stocks'

    paginated_stocks = call(url, 'POST', None, get_all_stocks_req, retry_count, raise_exception)

    return paginated_stocks


"""
Get Current Holding Stk Data

"""

def get_current_holding_stks(retry_count=DEFAULT_RETRY_COUNT, raise_exception=True):
    url = f'https://{G_HOST}/v1/api/stocks_router/v6/dashboard?ts={datetime.datetime.now()}&source=other'
    req_headers = get_auth_headers()
    current_holding_response = call(url, 'GET', req_headers, None, retry_count, raise_exception)
    return current_holding_response




