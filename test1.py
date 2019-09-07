#!/usr/bin/env python3 
import feedparser
from pprint import pprint
import sys
d = feedparser.parse(sys.argv[1])

for each in d.entries:
    pprint(each.published_parsed)
    print()
    print()
