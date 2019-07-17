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
import config
from sql_alchemy_setup import Podcast, Episode
import operator
import json
import re

def main_menu():
    while True:
        os.system('clear')
        print('number 1 add new podcast')
        print('number 2 edit existing podcast')
        print('number 3 delete existing podcast')
        print('number 4 choose episodes to download')
        print('number 5 start downloads')
        print('number 6 search for podcasts')
        print('number 7 list podcasts')
        result = input('choice ')
        try:
            result = int( result )
            if result == 1:
                add_new_podcast(Podcast())
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
            elif result == 6:
                search()
            elif result == 7:
                list_podcasts()

                
        except ValueError:
            if result == 'q':
                break

def list_podcasts():
    podcasts = sql.get_all_podcasts()
    print_out_menu_options(podcasts)

def search():
    os.system('clear')
    terms = input('Enter search terms: ')
    url = "https://itunes.apple.com/search?term={0}&entity=podcast&limit=200".format(terms)
    response = requests.get(url)
    data = json.loads(response.content)
    results = []
    for each in data['results']:
        if 'feedUrl' in each:
            podcast = Podcast(each['artistName'].lower() + "-" +each['collectionName'].lower() ,each['feedUrl'],config.audio_default_location, config.video_default_location)
            
            results.append(podcast)

    choices = print_out_menu_options(results,True)
    if choices is not None:
        for each in choices:
            add_new_podcast(each)

def update_episodes(podcast):
    ep = sql.get_episodes_by_podcast_id(podcast) 
    ep2 = backend.get_podcast_data_from_feed(podcast.url)

    
    for each in ep:
        try:
            ep2.remove(each)
        except Exception:
            pass

    for each in ep2:
        each.podcast_id = podcast.podcast_id

    sql.insert_episodes(ep2)



# def input_with_timeout(prompt, timemount=5):
#     timer = threading.Timer()

def enter_podcast_info(podcast):
    try:
        os.system('clear')
        while True:
            # add a check for names to this section
            # podcast.name = re.sub(r'(\s)+', '-', podcast.name)
            podcast.name = rlinput( 'podcast name ', podcast.name )
            if len(podcast.name) > 0:
                break
            else:
                print('nothing entered')

        while True:
            podcast.url =  rlinput( 'podcast url ', podcast.url )
            if backend.check_feed(podcast.url):
                break
            else:
                print('that url did not work')
        
        while True:
            if len(podcast.audio) == 0:
                podcast.audio = config.audio_default_location
            podcast.audio = rlinput( 'podcast audio directory ', podcast.audio )
            if os.path.isdir(podcast.audio):
                break
            else:
                print('that directory does not exist')

        while True:
            if len(podcast.video) == 0:
                podcast.video = config.video_default_location
            podcast.video = rlinput( 'podcast video directory ', podcast.video )
            if os.path.isdir(podcast.video):
                break
            else:
                print('that directory does not exist')
        return podcast
    except KeyboardInterrupt:
        podcast = None
        return podcast
    except:
        raise




def add_new_podcast(podcast):
    podcast = enter_podcast_info(podcast)
    if podcast != None:
        episodes = backend.get_podcast_data_from_feed(podcast.url)
        sql.insert_podcast2(podcast,episodes)

def edit_existing_podcast(podcast):
    enter_podcast_info(podcast)
    if podcast != None:
        episodes = backend.get_podcast_data_from_feed(podcast.url)
        sql.delete_episodes_by_podcast_id(podcast)
        sql.update_podcast2(podcast,episodes)

# def delete_existing_podcast(podcast):
#     backend.remove_podcast(podcast)

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
        each.percent = 0
    for i,each in enumerate(download_queue):
        filename =  each.href.split('/')[-1]
        extension_start = filename.split('.')
        extension = extension_start[len(extension_start)-1]
        dl_location = ''
        podcast = sql.get_podcast_by_id2(each) 
        filename2 = podcast.name
        if each.audio == 1:
            dl_location = podcast.audio #[0]['audio']
        else:
            dl_location = podcast.video #[0]['video']
        
        filename2 += "-" + each.title.replace(" ", "-").lower() +"."+extension

        print('saving {} - {} of {}'.format(filename2, i+1, len(download_queue)))
        
        with open(dl_location + '/' + filename2, 'wb')as f:
            r = requests.get(each.href, stream=True)
            total_length = int( r.headers.get('content-length') )
            dl = 0
            if total_length is None: # no content length header
                f.write(r.content)
            else:
                for chunk in r.iter_content(1024):
                    dl += len(chunk)
                    f.write(chunk)
                    done = int(100 * dl / total_length)
                    download_queue[i].percent = done

        sql.update_episode_as_downloaded(each) 
    
    download_queue.clear()





def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()
    


def print_out_menu_options(options, multi_choice=False, func=None):
    try:
        options.sort(key=lambda x: x.name)
    except AttributeError:
        pass

    try:
        options.sort(key=lambda x: x.title)
    except AttributeError:
        pass 

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
            try:
                print( 'number {} {}'.format(each + 1, options[each].name) )
            except AttributeError:
                pass

            try:
                print( 'number {} {}'.format(each + 1, options[each].title) )
            except AttributeError:
                pass
            # if hasattr(options[each], 'name'):
            # if 'name' in options[each]:
            #     print( 'number {} {}'.format(each + 1, options[each].name) )
            # elif 'title' in options[each]:
            # # elif hasattr(options[each], 'title'):
            #     print( 'number {} {}'.format(each + 1, options[each].title) )

            # if 'name' in options[each]:
            #     print( 'number {} {}'.format(each, options[each]['name']) )
            # elif 'title' in options[each]:
            #     print( 'number {} {}'.format(each, options[each]['title']) )

        result = input('choice ')        
        try:
            result = int(result)
            if result <= len(options):
                if multi_choice and func:
                    func( options[result-1] ) 
                elif multi_choice:
                    choices.append(options[result-1])
                elif func:
                    func( options[result-1] )
                else: 
                    return options[result-1]
            
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
sql = DatabaseAccessor(config.database_location)
backend = Backend(sql)
#update podcasts
podcasts = sql.get_all_podcasts()
itx = 1
for each in podcasts:
    print('updating {} of {}'.format(itx, len(podcasts)))
    itx += 1
    update_episodes(each)

main_menu()
