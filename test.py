#!/usr/bin/env python3 
import config
import pickle
from pprint import pprint
import sys

import requests
from bs4 import BeautifulSoup
import os
import subprocess
import math
import json
import pprint as pp
import time
import sys
import urllib.parse
# pprint(vars(your_object))

# result = 'Mon, 24 Jun 2019 15:30:00 -0400'
# result = 'Mon, 24 Jun 2019 15:30:00 -0400'

# import datetime

# # res = datetime.datetime.strptime(result, '%a, %W %b %Y %H:%I:%S %z') 
# res = datetime.datetime.strptime(result, '%a, %W %b %Y %H:%M:%S %z') 
# print(res)


# examining state.obj

# end =set()
# state = open('/home/marc/Desktop/podcatcher/state.obj', 'rb') 
# result = pickle.load(state)
# for each in result:
#     try: 
#         # print(each)
#         end.add(each.episode_id)
#     except Exception:
#         print('problem')
        
#     # pprint(vars(each))
#     # print(each.title)

# for each in end:
#     print(each)

# state2 = open('/home/marc/Desktop/podcatcher/state2.obj', 'wb')
# pickle.dump(end, state2)



# find string length
# string = sys.argv[1]
# count = 0
# for each in string:
#     count+=1

# print(count)


def get_script(url):
    page = requests.get( url )
    soup = BeautifulSoup(page.content, 'html.parser')
    scripts = soup.find_all('script')
    res2 = ''
    for each in scripts:
        if 'window.__IPLAYER_REDUX_STATE__ = ' in each.text:
            res2 = each.text.replace('window.__IPLAYER_REDUX_STATE__ = ','')
            res2 = res2.replace(';','')

    # pp.pprint(res2)
    # time.sleep(5)
    return soup
    return json.loads(res2)



u = "https://abcnews.go.com/Live"

result = get_script(u)

pprint(result)