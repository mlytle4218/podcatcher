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
from sql_alchemy_setup import Podcast, Episode, Category
import operator
import json
import re
import pickle

def main_menu():
    while True:
        os.system('clear')
        print('number 1 add category')
        print('number 2 edit category')
        print('number 3 add new podcast')
        print('number 4 edit existing podcast')
        print('number 5 delete existing podcast')
        print('number 6 choose episodes to download')
        print('number 7 start downloads')
        print('number 8 search for podcasts')
        print('number 9 list podcasts')
        print('number 10 search by category')
        result = input('choice ')
        try:
            result = int( result )
            if result == 3:
                add_new_podcast(Podcast())
            elif result == 4:
                edit_existing_podcast()
            elif result == 5:
                podcasts = sql.get_all_podcasts()
                choice = print_out_menu_options(podcasts, 'name', False, None, True)
                if choice != None:
                    sql.delete_podcast2(choice)
            elif result == 6:
                choose_episodes_to_download()
            elif result == 7:
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
            elif result == 8:
                search()
            elif result == 9:
                list_podcasts()
            elif result == 1:
                add_category()
            elif result == 10:
                search_by_category()
            elif result == 20:
                os.system('clear')
                for pod in download_queue:
                    print(pod)

                time.sleep(5)
                #     sql.log( str( pod ))
            elif result == 2:
                edit_category()

                
        except ValueError:
            if result == 'q':
                break

def search_by_category():
    categories = sql.get_all_categories()
    choice = print_out_menu_options(categories, 'category', False, False, False)
    if choice is not None:
        podcasts = sql.get_all_podcasts_with_category(choice)
        print_out_menu_options(podcasts, 'name', False, list_episodes, True)

def edit_category():
    categories = sql.get_all_categories()
    choice = print_out_menu_options(categories, 'category', False, False, False)
    sql.log( str( type( choice) ) )
    if choice is not None:
        choice.category = rlinput( 'category name: ', choice.category).strip()
        # pass
        # podcast.url =  rlinput( 'podcast url ', podcast.url ).strip()


def add_category():
    try:
        os.system('clear')
        while True:
            category_name = input('Enter category name: ')
            if len(category_name) == 0:
                break
            category = Category(category_name)
            result = sql.add_new_category(category)
            if not result:
                print('{} could not be added as a category'.format(category_name))
            else:
                break
    except KeyboardInterrupt:
        pass



def list_podcasts():
    podcasts = sql.get_all_podcasts()
    print_out_menu_options(podcasts, 'name', False, None, True)

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

    choices = print_out_menu_options(results, 'name', True, None, True)
    if choices is not None and isinstance(choices, Podcast):
        add_new_podcast(choices)
    elif choices is not None:
        for each in choices:
            add_new_podcast(each)
    

def update_episodes_old(podcast):
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

def update_episodes(podcast):
    try:
        existing_episodes = sql.get_episodes_by_podcast_id(podcast)
        temp_existing_episodes = existing_episodes[:]
        retreived_episodes = backend.get_podcast_data_from_feed(podcast.url)

        # this take each retrieved episode and tries to remove it from the 
        # local data. If it fails, then the local data doesn't have it and it
        # needs to added
        for each in retreived_episodes:
            try:
                existing_episodes.remove(each)
            except Exception:
                each.podcast_id = podcast.podcast_id
                result = sql.add_episode(each)


        # this takes each existing episode and tries to remove it from the 
        # retrieved episodes. If it fails, then the retrieved data doesn't have it
        # which means it is no longer available. I therefore has to be removed from the
        # local data.
        for each in temp_existing_episodes:
            try:
                retreived_episodes.remove(each)
            except Exception:
                result = sql.delete_episode(each)

        return True
    except Exception as e:
        sql.log( str( e ) )
        return False

def enter_podcast_info(podcast):
    try:
        os.system('clear')
        # add a check for names to this section
        # podcast.name = re.sub(r'(\s)+', '-', podcast.name)
        while True:
            podcast.name = rlinput( 'podcast name ', podcast.name )
            if len(podcast.name) > 0:
                break
            else:
                print('nothing entered')
        # check the url works 
        while True:
            podcast.url =  rlinput( 'podcast url ', podcast.url ).strip()
            if backend.check_feed(podcast.url):
                break
            else:
                print('that url did not work')
        
        # check the audio path
        while True:
            if len(podcast.audio) == 0:
                podcast.audio = config.audio_default_location
            podcast.audio = rlinput( 'podcast audio directory ', podcast.audio )
            if os.path.isdir(podcast.audio):
                break
            else:
                print('that directory does not exist')

        # check the video path
        while True:
            if len(podcast.video) == 0:
                podcast.video = config.video_default_location
            podcast.video = rlinput( 'podcast video directory ', podcast.video )
            if os.path.isdir(podcast.video):
                break
            else:
                print('that directory does not exist')

        # check categories
        while True:
            # check if the category is set - print it if it is
            if podcast.category:# and  len(podcast.category) != 0:
                print("category: {}".format(podcast.category))
            # retrieve all the categories
            categories = sql.get_all_categories()
            # if there are categories - show them - if not ask for a category
            if len(categories) > 0:
                for i,cat in enumerate(categories):
                    print("number {} for {}".format(i+1, cat))
                result = input('choice: ')
            else:
                result = input('enter new category: ')
            # see if the result is a number and thusly a choice from the menu
            # else assume either no entry, q for quit, or the new category
            try:
                result = int(result)
                podcast.category = categories[result-1].category
                break
            except  ValueError:
                if len(result) == 0:
                    break
                if result == 'q':
                    break
                # add new category
                added = sql.add_new_category(result)
                if added:
                    podcast.category = result
                    break
                else:
                    print("could not add that category")

        
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

def edit_existing_podcast():
    try:
        podcasts = sql.get_all_podcasts()
        podcast = print_out_menu_options(podcasts, 'name', False, None, True)
        if podcast != None:
            enter_podcast_info(podcast)
            if podcast != None:
                episodes = backend.get_podcast_data_from_feed(podcast.url)
                sql.delete_episodes_by_podcast_id(podcast)
                sql.update_podcast2(podcast,episodes)
    except KeyboardInterrupt as e:
        sql.log( str( e ) )

def edit_existing_podcast2(podcast):
    enter_podcast_info(podcast)
    if podcast != None:
        episodes = backend.get_podcast_data_from_feed(podcast.url)
        sql.delete_episodes_by_podcast_id(podcast)
        sql.update_podcast2(podcast,episodes)

def choose_episodes_to_download():
    podcasts  = sql.get_podcasts_with_downloads_available()
    print_out_menu_options(podcasts, 'name', False, list_episodes, True)

def list_episodes(podcast):
    episodes = sql.get_episodes_with_downloads_available(podcast)
    print_out_menu_options(episodes, 'title', True, add_to_download_queue, False)

def add_to_download_queue(episode):
    download_queue.append(episode)
    write_state_information()

def write_state_information():
    state = open(config.pickled_file_location, 'wb')
    # d = Category('tom')
    pickle.dump(download_queue, state)

def read_state_information():
    state = open(config.pickled_file_location, 'rb') 
    return pickle.load(state)

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
    


def print_out_menu_options(options, attribute, multi_choice, func, sort):
    if sort:
        options.sort(key=lambda x: getattr(x, attribute))
    if len(options) < 2:
        multi_choice = False

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
            print( 'number {} {}'.format( each + 1, getattr(options[ each ], attribute) ))

        result = input('choice ')     
        if result == 'n':
            if page_itr < len(display_control) -1:
                page_itr +=1
        elif result =='p':
            if page_itr > 0:
                page_itr -=1
        elif result =='q':
            if len(choices) > 0:
                return choices
            break
        else: 
            # this is looking for entries that are in the form 1-4 to represent 
            # choices 1,2,3,4 - requested option
            # first separate out the 1-4 options whether they have spaces in betweeen
            # the numbers and dashes or not
            dashed_option_choices = re.findall(r'[0-9]{1,2}\ ?\-\ ?[0-9]{1,2}', result)
            result = re.sub(r'[0-9]{1,2}\ ?\-\ ?[0-9]{1,2}','', result)
            result_list = result.split(' ')

            for each in dashed_option_choices:
                each_list = each.split('-')
                try:
                    for i in range(int(each_list[0]), int(each_list[1])+1):
                        result_list.append(i)
                except ValueError:
                    pass

            result_list2 = []
            
            for each in result_list:
                if isinstance(each, str):
                    if len(each) > 0:
                        result_list2.append(each)
                else:
                    result_list2.append(each)

            for item in result_list:
                try:
                    item = int(item)
                    if item <= len(options):
                        if multi_choice and func:
                            func( options[ item - 1 ] )
                        elif multi_choice:
                            choices.append(options[item-1])
                        elif func:
                            func( options[ item-1 ] )
                        else:
                            return options[item-1]
                except ValueError:
                    pass


width = int( subprocess.check_output(['tput','cols']) )
height = int( subprocess.check_output(['tput','lines']) ) -1

download_queue = read_state_information()
sql = DatabaseAccessor(config.database_location)
backend = Backend(sql)
# update podcasts
# podcasts = sql.get_all_podcasts()
# itx = 1
# for each in podcasts:
#     result = update_episodes(each)
#     if result:
#         print('updated {} : {} of {}'.format(each.name, itx, len(podcasts)))
#         itx += 1
#     else:
#         print('problem updating {} : {}  of {}'.format( each.name, itx, len(podcasts)  ))
# time.sleep(1)

main_menu()
