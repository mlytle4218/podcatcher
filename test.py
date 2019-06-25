#!/usr/bin/env python3 

# result = 'Mon, 24 Jun 2019 15:30:00 -0400'
result = 'Mon, 24 Jun 2019 15:30:00 -0400'

import datetime

# res = datetime.datetime.strptime(result, '%a, %W %b %Y %H:%I:%S %z') 
res = datetime.datetime.strptime(result, '%a, %W %b %Y %H:%M:%S %z') 
print(res)

