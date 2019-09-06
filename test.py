#!/usr/bin/env python3 
import config
import pickle
from pprint import pprint
# pprint(vars(your_object))

# result = 'Mon, 24 Jun 2019 15:30:00 -0400'
# result = 'Mon, 24 Jun 2019 15:30:00 -0400'

# import datetime

# # res = datetime.datetime.strptime(result, '%a, %W %b %Y %H:%I:%S %z') 
# res = datetime.datetime.strptime(result, '%a, %W %b %Y %H:%M:%S %z') 
# print(res)


end =set()
state = open('/home/marc/Desktop/podcatcher/state.obj', 'rb') 
result = pickle.load(state)
for each in result:
    try: 
        # print(each)
        end.add(each.episode_id)
    except Exception:
        print('problem')
        
    # pprint(vars(each))
    # print(each.title)

for each in end:
    print(each)

state2 = open('/home/marc/Desktop/podcatcher/state2.obj', 'wb')
pickle.dump(end, state2)