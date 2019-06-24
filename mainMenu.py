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
                podcasts = backend.get_podcasts()
                choice = print_out_menu_options(podcasts)
                if choice != None:
                    edit_existing_podcast(choice)
            elif result == 3:
                podcasts = backend.get_podcasts()
                choice = print_out_menu_options(podcasts)
                if choice != None:
                    delete_existing_podcast(choice)
            elif result == 4:
                choose_episodes_to_download()
            elif result == 5:
                # start_downloads()
                t1 = threading.Thread(target=start_downloads)
                t1.start()
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


def add_new_podcast():
    os.system('clear')
    podcast = {}
    podcast['name'] = input( 'podcast name ' )
    podcast['url'] =  input( 'podcast url ' )
    podcast['audio'] = input( 'podcast audio ' )
    podcast['video'] = input( 'podcast video ' )
    id = backend.add_new_podcast(podcast)

def edit_existing_podcast(podcast):
    podcast['name'] = rlinput('name ', podcast['name'])
    podcast['url'] = rlinput('url ', podcast['url'])
    podcast['audio'] = rlinput('audio ', podcast['audio'])
    podcast['video'] = rlinput('video ', podcast['video'])
    backend.update_podcast(podcast)

def delete_existing_podcast(podcast):
    backend.remove_podcast(podcast)

def choose_episodes_to_download():
    podcasts = backend.get_podcasts_that_have_downloads_available()
    print_out_menu_options(podcasts, False, list_episodes)

def list_episodes(podcast):
    episodes = backend.get_episodes_that_have_downloads_available_from_podcast_id(podcast)
    print_out_menu_options(episodes, True, add_to_download_queue)

def add_to_download_queue(episode):
    download_queue.append(episode)

def start_downloads():
    for each in download_queue:
        each['percent'] = 0
    for i,each in enumerate(download_queue):
        filename =  each['url'].split('/')[-1]
        dl_location = ''
        podcast = backend.get_download_location_from_podcast_id(each['podcast_id']) 
        if each['audio'] == 1:
            backend.log( str( podcast ) )
            dl_location = podcast[0]['audio']
        else:
            dl_location = podcast[0]['video']
        
        with open(dl_location + '/' + filename, 'wb')as f:
            r = requests.get(each['url'], stream=True)
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
                    # result =  "[{}{}] {} bps".format(done, 50-done, dl/(time.clock() - start))
                    # result = " {}%".format(done)
                    # backend.log( result )
        
        backend.update_episode_as_downloaded(each) 





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
sql = DatabaseAccessor('pc_database.db')
backend = Backend(sql)
main_menu()
