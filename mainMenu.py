#!/usr/bin/env python3
import os
import subprocess
import math 
from new import Backend
from sql import DatabaseAccessor
import readline
import requests
import time
import threading


def main_menu():
    while True:
        os.system('clear')
        print('number 1 add new podcast')
        print('number 2 edit existing podcast')
        print('number 3 delete existing podcast')
        print('number 4 choose episodes to download')
        print('number 5 start downloads')
        result = input('choice ')
        try:
            result = int( result )
            if result == 1:
                add_new_podcast()
            elif result == 2:
                podcasts = sql.get_all_podcasts()
                choice = print_out_menu_options(podcasts)
                if choice != None:
                    edit_existing_podcast(choice)
            elif result == 3:
                podcasts = sql.get_all_podcasts()
                choice = print_out_menu_options(podcasts)
                if choice != None:
                    sql.delete_podcast2(choice)
                    # delete_existing_podcast(choice)
            elif result == 4:
                choose_episodes_to_download()
            elif result == 5:
                start_downloads()
                # t1 = threading.Thread(target=start_downloads)
                # t1.start()
                # t1.join()
                # while True:
                #     os.system('clear')
                #     for each in download_queue:
                #         print( "{}% {}".format(
                #             each['percent'],each['title']
                #         ) )
                
        except ValueError:
            if result == 'q':
                break

# def input_with_timeout(prompt, timemount=5):
#     timer = threading.Timer()

def enter_podcast_info(podcast):
    os.system('clear')
    while True:
        if 'name' not in podcast:
            podcast['name'] = ''
        podcast['name'] = rlinput( 'podcast name ', podcast['name'] )
        if len(podcast['name']) > 0:
            break
        else:
            print('nothing entered')

    while True:
        if 'url' not in podcast:
            podcast['url'] = ''
        podcast['url'] =  rlinput( 'podcast url ', podcast['url'] )
        if backend.check_feed(podcast['url']):
            break
        else:
            print('that url did not work')
    
    while True:
        if 'audio' not in podcast:
            podcast['audio'] = ''
        podcast['audio'] = rlinput( 'podcast audio directory ', podcast['audio'] )
        if os.path.isdir(podcast['audio']):
            break
        else:
            print('that directory does not exist')

    while True:
        if 'video' not in podcast:
            podcast['video'] = ''
        podcast['video'] = rlinput( 'podcast video directory ', podcast['video'] )
        if os.path.isdir(podcast['video']):
            break
        else:
            print('that directory does not exist')






def add_new_podcast():
    podcast = {}
    enter_podcast_info(podcast)
    episodes = backend.get_podcast_data_from_feed(podcast['url'])
    sql.insert_podcast2(podcast,episodes)
    # podcast['name'] = input( 'podcast name ' )
    # podcast['url'] =  input( 'podcast url ' )
    # podcast['audio'] = input( 'podcast audio ' )
    # podcast['video'] = input( 'podcast video ' )
    # if backend.check_feed(podcast['url']):
    #     episodes = backend.get_podcast_data_from_feed(podcast['url'])
    #     sql.insert_podcast2(podcast,episodes)

def edit_existing_podcast(podcast):
    enter_podcast_info(podcast)
    episodes = backend.get_podcast_data_from_feed(podcast['url'])
    sql.delete_episodes_by_podcast_id(podcast)
    sql.update_podcast2(podcast,episodes)
    # podcast['name'] = rlinput('name ', podcast['name'])
    # podcast['url'] = rlinput('url ', podcast['url'])
    # podcast['audio'] = rlinput('audio ', podcast['audio'])
    # podcast['video'] = rlinput('video ', podcast['video'])
    # if backend.check_feed(podcast['url']):
    #     episodes = backend.get_podcast_data_from_feed(podcast['url'])
    #     sql.delete_episodes_by_podcast_id(podcast)
    #     sql.update_podcast2(podcast,episodes)

def delete_existing_podcast(podcast):
    backend.remove_podcast(podcast)

def choose_episodes_to_download():
    podcasts  = sql.get_podcasts_with_downloads_available()
    print_out_menu_options(podcasts, False, list_episodes)

def list_episodes(podcast):
    episodes = sql.get_episodes_with_downloads_available(podcast)
    print_out_menu_options(episodes, True, add_to_download_queue)

def add_to_download_queue(episode):
    download_queue.append(episode)

def start_downloads():
    for each in download_queue:
        each['percent'] = 0
    for i,each in enumerate(download_queue):
        filename =  each['href'].split('/')[-1]
        print('saving {} - {} of {}'.format(filename, i+1, len(download_queue)))
        dl_location = ''
        podcast = sql.get_podcast_by_id2(each) 
        if each['audio'] == 1:
            dl_location = podcast.audio #[0]['audio']
        else:
            dl_location = podcast[0]['video']
        
        with open(dl_location + '/' + filename, 'wb')as f:
            # sql.log( str( dl_location+"/"+filename ) )
            r = requests.get(each['href'], stream=True)
            total_length = int( r.headers.get('content-length') )
            dl = 0
            if total_length is None: # no content length header
                f.write(r.content)
            else:
                for chunk in r.iter_content(1024):
                    dl += len(chunk)
                    f.write(chunk)
                    done = int(100 * dl / total_length)
                    download_queue[i]['percent'] = done

        sql.update_episode_as_downloaded(each) 
    
    download_queue.clear()





def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()
    


def print_out_menu_options(options, multi_choice=False, func=None):
    choices = []
    full = int( math.floor(len(options) / height ) )
    remainder = len(options) - (full * height)


    display_control = []
    counter = 0
    for each in range(full):
        temp = []
        for itr in range(height):
            temp.append(counter)
            counter+=1

        display_control.append(temp)
    temp = []
    for each in range(remainder):
        temp.append(counter)
        counter+=1
    
    display_control.append(temp)
    
    page_itr = 0

    while True:
        os.system('clear')
        for each in display_control[page_itr]:
            # sql.log( str( options[each] ) )
            if 'name' in options[each]:
                print( 'number {} {}'.format(each, options[each]['name']) )
            elif 'title' in options[each]:
                print( 'number {} {}'.format(each, options[each]['title']) )

        result = input('choice ')        
        try:
            result = int(result)
            if result <= len(options):
                if multi_choice and func:
                    func( options[result] ) 
                elif multi_choice:
                    choices.append(options[result])
                elif func:
                    func( options[result] )
                else: 
                    return options[result]
            
        except ValueError:
            if result == 'n':
                if page_itr < len(display_control) -1:
                    page_itr +=1
            elif result =='p':
                if page_itr > 0:
                    page_itr -=1
            elif result =='q':
                # if len( download_queue ) > 0:
                #     backend.log( str( download_queue ) )
                break
            elif multi_choice and result =='d':
                return choices


width = int( subprocess.check_output(['tput','cols']) )
height = int( subprocess.check_output(['tput','lines']) ) -1

download_queue = []
sql = DatabaseAccessor('/home/marc/Desktop/podcatcher/pc_database.db')
backend = Backend(sql)
main_menu()
