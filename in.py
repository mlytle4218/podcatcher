#!/usr/bin/env python3
import sys,os
import subprocess
import math
from new import Backend
from sql import DatabaseAccessor
import readline
import requests
import time
# import threading
import config
from sql_alchemy_setup import Podcast, Episode, Category
# import operator
import json
import re
import pickle
import sql


print(os.path.isdir('/home'))
print(os.path.isdir('/bell'))
print(os.path.isdir(config.audio_default_location))







#directory = sys.argv[1]
#directory = config.audio_default_location
#result = os.path.isdir(directory)

#print(result)
# for root_here, dirs_here, files_here in os.walk('/'):
#         # for name in files:
#         #     sql.log(str(os.path.join(root, name)))
#         for name_here in dirs_here:
#             try:
#                  #print(str(os.path.join(root_here, name_here)))
#                  if name_here:
#                      pass
#             except Exception as e:
#                 print(e)
