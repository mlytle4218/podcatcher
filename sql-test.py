#!/usr/bin/env python3
import subprocess
from sql import DatabaseAccessor
import config
from sql_alchemy_setup import Category


width = int( subprocess.check_output(['tput','cols']) )
height = int( subprocess.check_output(['tput','lines']) ) -1

download_queue = []
sql = DatabaseAccessor(config.database_location)

category = 'eric'

insert_result = sql.add_new_category(category)
print("insert_result:{}".format(insert_result))

cats = sql.get_all_categories()

for each in cats:
    print(each)

results = sql.get_all_podcasts_with_category(Category(category))

for each in results:
    print(each)
