
import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup



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
    url = f'https://www.google.com/search?q={query}'
    api_response = requests.request(url=url, method='GET', headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}, verify=False)
    soup = BeautifulSoup(api_response.content, 'html.parser')
    x_tags = soup.find_all('a', jsname='UWckNb', recursive=True)
    for tag in x_tags:
        print(tag.get('href'))


