
import sys, requests, concurrent.futures, math
from bs4 import BeautifulSoup
from plyer import notification
from gapis.apis import *
from hermes.crud import *


CURSOR_UP_ONE               = '\x1b[1A' 
ERASE_LINE                  = '\x1b[2K' 

GLOBAL_THREAD_POOL          = None

def clear_line():
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE) 


def trigger_notification(notification_title, notification_msg):
    notification.notify( title = f'{notification_title}', message = f'{notification_msg}', timeout = 2)


"""
Sorts the given stk objects
"""
def sort_dict(dict_list, sort_key, start_idx, end_idx):
    
    if( start_idx>-1 and end_idx>-1 and start_idx<end_idx and (dict_list[start_idx][sort_key] is not None) and (dict_list[end_idx][sort_key] is not None)):
        pivot_ele_idx = start_idx
        i = start_idx
        j = end_idx

        while(i<j):
            
            while(i<end_idx and dict_list[i][sort_key]<=dict_list[pivot_ele_idx][sort_key]):
                i+= 1

            while(j>start_idx and dict_list[pivot_ele_idx][sort_key]<=dict_list[j][sort_key]):
                j-= 1

            if(i<j):

                tmp_dict = dict_list[j]
                dict_list[j] = dict_list[i]
                dict_list[i] = tmp_dict

        tmp_dict = dict_list[j]
        dict_list[j] = dict_list[pivot_ele_idx]
        dict_list[pivot_ele_idx] = tmp_dict

        sort_dict(dict_list, sort_key, start_idx, j-1)
        sort_dict(dict_list, sort_key, j+1, end_idx)



"""
Finds the length of longest unaltered subarry candles and returns the length
"""
def longest_unchanged_price_subset_length(candles):
    longest_len = 1
    current_len = 1
    
    for i in range(0,len(candles)-1):
        if(candles[i][1]==candles[i+1][1]):
            current_len+=1
            longest_len = max(current_len, longest_len)
        else:
            current_len=1

    return longest_len



def get_google_results(query):
    requests.packages.urllib3.disable_warnings()
    url = f'https://www.google.com/search?q={query}'
    api_response = requests.request(url=url, method='GET', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}, verify=False)
    soup = BeautifulSoup(api_response.content, 'html.parser')
    x_tags = soup.find_all('a', jsname='UWckNb', recursive=True)
    links = []
    for tag in x_tags:
        links.append(tag.get('href'))
    return links


"""
Initiates the threadpool for firing concurrent requests
"""

def get_thread_pool():
    global GLOBAL_THREAD_POOL
    if(GLOBAL_THREAD_POOL is None):
        GLOBAL_THREAD_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    return GLOBAL_THREAD_POOL


"""
Shuts threadpool down if it is active or open.
"""

def shutdown_thread_pool():
    global GLOBAL_THREAD_POOL
    if(GLOBAL_THREAD_POOL is not None):
        GLOBAL_THREAD_POOL.shutdown(wait=True)


"""
Iterates through all the pages and executes the given functions.
func should return a list output which can be appended in each iteration with previous output

"""

def process_all_gstks(func, output = [], page_number = 0, page_size = DEFAULT_API_PAGE_SIZE, iteration_threshold = DEFAULT_ITERATION_LIMIT, raise_exception = True):
    
    if(iteration_threshold<=0):
        iteration_threshold = DEFAULT_ITERATION_LIMIT

    has_more_stocks = True

    while(iteration_threshold>0 and has_more_stocks):

        print(f'PageNumber: {page_number} PageSize: {page_size} ThresholdCount: {iteration_threshold} HasMoreStocks: {has_more_stocks}')

        paginated_stock_list = get_gstk_page(page=page_number, size=page_size, raise_exception=raise_exception)
        func_output = func(paginated_stock_list['records'])
        
        if(isinstance(func_output, list)):
            output += func_output

        has_more_stocks = ( paginated_stock_list['totalRecords'] - ((page_number+1)*page_size) ) > 0
        iteration_threshold-= 1
        page_number+= 1


######################### ITERATE STKS FROM DB #############################

def process_all_db_stks(func, output = [], batch_start_idx = 0, batch_size = DEFAULT_DB_BATCH_SIZE, iteration_threshold = DEFAULT_ITERATION_LIMIT):

    if (iteration_threshold<=0 or iteration_threshold>=DEFAULT_ITERATION_LIMIT):
        iteration_threshold = math.ceil(get_stk_table_size()/batch_size)

    do_process = True

    
    while(do_process):
    
        print(f'Offset: {batch_start_idx} LimitTill: {batch_size} ThresholdCount: {iteration_threshold}')

        stks = get_all_stks(batch_start_idx, batch_size)

        func_output = func(stks)

        if(isinstance(func_output, list)):
            output += func_output

        iteration_threshold     -= 1
        batch_start_idx         += batch_size
        do_process              = iteration_threshold!=0

