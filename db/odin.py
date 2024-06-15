import mysql.connector
from conf.config import *



CNX         = None
CURSOR      = None

###################### CLOSE DB CONNECTION ###########################

def open_connection():
    global CNX, CURSOR

    if(CNX is None):
        CNX = mysql.connector.connect(user=DB_USER_NAME, host=DB_HOST, port= DB_PORT, database=DATABASE)

    if(CURSOR is None):
        CURSOR = CNX.cursor()

###################### OPEN DB CONNECTION ############################

def close_connection():
    global CNX, CURSOR

    if(CURSOR is not None):
        CURSOR.close()
        CNX.close()
        return

    if(CNX is not None):
        CNX.close()

########### UTILITY METHOD THAT CONVERTS LIST TO QUERY TUPLE ##########

def convert_to_query_tuple(list):
    
    list = sorted(list)
    
    if(len(list)==0):
        return '("")'
    
    query_tuple = '( ' + '\'' +list[0] + '\''

    for item in list[1:]:
        query_tuple+= ', ' + '\''+ item + '\''

    query_tuple+= ' )'

    return query_tuple


################## UPSERTS STK DATA IN DB ############################

def upsert_data(stk_data):

    select_query = 'SELECT * FROM gst_details WHERE  `search_id` IN (%s)'
    
    CURSOR.execute(select_query, ([stk_data.get('search_id')]))
    
    record_tuple = None

    for record in CURSOR:
        record_tuple = record
        break
    
    try:
        
        if(record_tuple == None):
            query = 'INSERT INTO `gst_details` (`search_id`, `exchange`, `code`, `g_contract_id`, `isin`) VALUES (%s, %s, %s, %s, %s)'
            parameter_tuple = (stk_data.get('search_id'), stk_data.get('exchange'), stk_data.get('code'), stk_data.get('g_contract_id'), stk_data.get('isin'))
            CURSOR.execute(query, parameter_tuple)
            # print(query, parameter_tuple)

        else:
            query = 'UPDATE `gst_details` SET `exchange`=%s, `code`=%s, `g_contract_id`=%s, `isin`=%s WHERE `search_id`=%s'
            parameter_tuple = (stk_data.get('exchange'), stk_data.get('code'), stk_data.get('g_contract_id'), stk_data.get('isin'), stk_data.get('search_id'))
            CURSOR.execute(query, parameter_tuple) 
            # print(query, parameter_tuple)
    
    except mysql.connector.Error as err:
        print(f'Error in Processing Upsert opertion for {stk_data.get("search_id")}<->{stk_data.get("exchange")}<->{stk_data.get("code")} \nError:{err}')

    CNX.commit()

############## TOGGLES TRADABLITY OF STOCK ###########################

def update_tradability(search_ids, tradability):
    
    try:
        query = f'UPDATE `gst_details` SET `tradable`={tradability} WHERE `search_id` in {convert_to_query_tuple(search_ids)}'
        CURSOR.execute(query) 
    except mysql.connector.Error as err:
        print(f'Error in Updating tradability \nError:{err}')

    CNX.commit()

############## FILTER OUT TRADABLE STK IDS ##########################

def get_tradable_search_ids(search_ids):

    select_query = f'SELECT search_id FROM gst_details WHERE `search_id` IN {convert_to_query_tuple(search_ids)} AND tradable = 1'
    
    CURSOR.execute(select_query)
    
    tradable_search_ids = []

    for record in CURSOR:
        tradable_search_ids.append(record[0])

    return tradable_search_ids


################# GET STK DETAILS FOR GIVEN SEARCH IDS ##############

def get_stk_details(search_id_list):
    select_query = f'SELECT * FROM gst_details WHERE `search_id` IN {convert_to_query_tuple(search_id_list)}'
    CURSOR.execute(select_query)
    stock_details = []
    for record in CURSOR:
        stock_detail = {}
        stock_detail['search_id'] = record[0]
        stock_detail['exchange'] = record[1]
        stock_detail['code'] = record[2]
        stock_details.append(stock_detail)
    return stock_details

################# GET SEARCH ID FROM DB###############################

def get_search_id_from_db(limit_start_idx, limit):
    select_query = f'SELECT `search_id` FROM gst_details LIMIT {limit_start_idx}, {limit}'
    CURSOR.execute(select_query)
    search_id_list = []
    for record in CURSOR:
        search_id = record[0]
        search_id_list.append(search_id)
    return search_id_list

################# COUNT OF STK IN DB ###############################  

def get_stk_cnt():
    select_query = f'SELECT COUNT(1) FROM gst_details'
    CURSOR.execute(select_query)
    for record in CURSOR:
        return record[0]

####################################################################


