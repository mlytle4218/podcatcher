#!/usr/bin/env python3 
import feedparser
from pprint import pprint
import sys
import re
import urllib
import requests
import shutil
import datetime

import subprocess
import multiprocessing
import time




print("Recording video...")
a = datetime.datetime.now()
url = "http://stream1.skyviewnetworks.com:8010/MSNBC"
# url="http://abc-news.akacast.akamaistream.net/7/730/126490/v1/espn.akacast.akamaistream.net/abc-news"
# url="http://amdlive-ch03.ctnd.com.edgesuite.net/arirang_3ch/smil:arirang_3ch.smil/chunklist_b1728000_sleng.m3u8"
filename = 'bob.data'
block_size = 1024
timer = 0


def ffmpeg(input):
    print(input)
    pipeline = ['ffmpeg','-y','-i',url,'out.mp3']
    p = subprocess.Popen(pipeline, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out = p.communicate()[0]

proc = multiprocessing.Process(target=ffmpeg)
proc.start('tom')
while timer < 60:
    time.sleep(0.5)
    timer += 1
proc.terminate()
