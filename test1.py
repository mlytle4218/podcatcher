#!/usr/bin/env python3 
import feedparser
from pprint import pprint
import sys
import re



bob1 = 'Fri, 08 Nov 2019 01:39:24 CST'
p = re.compile('^[a-zA-Z]{3}, [0-9]{2} [a-zA-Z]{3} [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}')
result = p.findall(bob1)
print(result[0])
# d = feedparser.parse(sys.argv[1])

# for each in d.entries:
#     pprint(each)
#     print()
#     print()
