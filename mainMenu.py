#!/usr/bin/env python3
import os
import subprocess
import math
from new import Backend
from sql import DatabaseAccessor
import readline
import requests
import time
import config
from sql_alchemy_setup import Podcast, Episode, Category
import json
import re
import pickle
import sys

def main_menu():
    try:
        if len(sys.argv) >1 and sys.argv[1] == '-u':
            sql.log('tried to update')
            update_all_episodes()

        else:
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
                print('number 9 delete from download queue')
                print('number 10 update all podcasts')
                print('number 11 archive')
                result = input('choice ')
                try:
                    result = int(result)
                    if result == 1:
                        add_category()
                    elif result == 2:
                        edit_category()
                    elif result == 3:
                        add_new_podcast(Podcast())
                    elif result == 4:
                        edit_existing_podcast()
                    elif result == 5:
                        delete_existing_podcast()
                    elif result == 6:
                        choose_episodes_to_download()
                    elif result == 7:
                        start_downloads()
                    elif result == 8:
                        search()
                    elif result == 9:
                        delete_from_download_queue()
                    elif result == 10:
                        update_all_episodes()
                    elif result == 11:
                        list_archived_episodes()

                    # hidden
                    elif result == 20:
                        for each in download_queue:
                            sql.log(vars(each))
                    elif result == 21:
                        update_episodes_fix()

                except ValueError:
                    if result == 'q':
                        break
    except KeyboardInterrupt:
        pass


def delete_existing_podcast():
    podcasts = sql.get_all_podcasts()
    choice = print_out_menu_options(podcasts, 'name', False, None, True)
    if choice is not None:
        sql.delete_podcast2(choice)


def delete_from_download_queue():
    choice = print_out_menu_options(download_queue, 'title', True, False, True)
    if choice is not None:
        if isinstance(choice, Episode):
            download_queue.remove(choice)
        else:
            for each in choice:
                download_queue.remove(each)
    write_state_information()


def list_archived_episodes():
    podcasts = sql.get_all_podcasts()
    print_out_menu_options(podcasts, 'name', False,
                           list_episodes_arch, True, True)


def update_all_episodes():
    sql.log('update all episodes')
    # update podcasts
    podcasts = sql.get_all_podcasts()
    itx = 1
    for each in podcasts:
        try:
            update_episodes(each)
            print('updated {} : {} of {}'.format(each.name, itx, len(podcasts)))
        except Exception as e:
            sql.log(e)
            print('problem updating {}'.format(each.name))
            time.sleep(1)
        itx += 1
    

def edit_category():
    categories = sql.get_all_categories()
    choice = print_out_menu_options(
        categories, 'category', False, False, False)
    # sql.log(str(type(choice)))
    if choice is not None:
        choice.category = rlinput('category name: ', choice.category).strip()
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


def search():
    os.system('clear')
    data = search_retrieval()
    if data != None:
        results = []
        for each in data['results']:
            if 'feedUrl' in each:
                newvariable486 = each['artistName'].lower() + "-" + each['collectionName'].lower( )
                newvariable486 = backend.remove_tags(newvariable486)
                podcast = Podcast(newvariable486, each['feedUrl'], config.audio_default_location, config.video_default_location)

                results.append(podcast)

        choices = print_out_menu_options(results, 'name', True, None, True)
        if choices is not None and isinstance(choices, Podcast):
            add_new_podcast(choices)
        elif choices is not None:
            for each in choices:
                add_new_podcast(each)


def search_retrieval():
    try:
        while  True:
            terms  = input('Enter search terms: ')
            url = "https://itunes.apple.com/search?term={0}&entity=podcast&limit=200".format(terms)
            response = requests.get(url, verify=False)
            data = json.loads(response.content)
            length = len(data['results'])
            if length > 0:
                return data
            print('{} results for: {}'.format(length, terms))
    except KeyboardInterrupt:
        return None


def update_episodes_old(podcast):
    ep = sql.get_episodes_by_podcast_id(podcast)
    ep2 = backend.get_episodes_from_feed(podcast.url)

    for each in ep:
        try:
            ep2.remove(each)
        except Exception:
            pass

    for each in ep2:
        each.podcast_id = podcast.podcast_id

    sql.insert_episodes(ep2)


def update_episodes_fix():
    pods = sql.get_all_podcasts()
    for pod in pods:
        retreived_episodes = backend.get_episodes_from_feed(pod.url)
        if retreived_episodes:
            sql.update_episodes_fix(retreived_episodes, pod)


def update_episodes(podcast):
    try:
        existing_episodes = sql.get_episodes_by_podcast_id(podcast)
        temp_existing_episodes = existing_episodes[:]
        retreived_episodes = backend.get_episodes_from_feed(podcast.url)

        # This next section is super inefficient needs to be adjusted to not suck

        # this take each retrieved episode and tries to remove it from the
        # local data. If it fails, then the local data doesn't have it and it
        # needs to added
        for each in retreived_episodes:
            try:
                existing_episodes.remove(each)
            except Exception:
                each.podcast_id = podcast.podcast_id
                result = sql.add_episode(each)
                if not result:
                    sql.log("problem adding {}".format(each))

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
        sql.log(str(e))
        return False


def enter_podcast_info(podcast):
    
    try:
        os.system('clear')
        # add a check for names to this section
        # podcast.name = re.sub(r'(\s)+', '-', podcast.name)
        while True:
            podcast.name = rlinput('podcast name ', podcast.name)
            if len(podcast.name) > 0:
                break
            else:
                print('nothing entered')
        # check the url works
        while True:
            podcast.url = rlinput('podcast url ', podcast.url).strip()
            if backend.check_feed(podcast.url):
                break
            else:
                print('that url did not work')

        # check the audio path
        while True:
            if len(podcast.audio) == 0:
                podcast.audio = config.audio_default_location
            podcast.audio = rlinput('podcast audio directory ', podcast.audio)

            if os.path.isdir(config.dl_prefix + podcast.audio):
                break
            else:
                print('{} does not exist'.format(podcast.audio))

        # check the video path
        while True:
            if len(podcast.video) == 0:
                podcast.video = config.video_default_location
            podcast.video = rlinput('podcast video directory ', podcast.video)
            if os.path.isdir(config.dl_prefix + podcast.video):
                break
            else:
                print('{} does not exist'.format(podcast.video))

        # check categories
        while True:
            # check if the category is set - print it if it is
            if podcast.category:
                print("category: {}".format(podcast.category))
            # retrieve all the categories
            categories = sql.get_all_categories()
            # if there are categories - show them - if not ask for a category
            if len(categories) > 0:
                for i, cat in enumerate(categories):
                    print("number {} for {}".format(i+1, cat))
                result = input('choice: ')
            else:
                result = input('enter new category: ')
            # see if the result is a number and thusly a choice from the menu
            # else assume either no entry, q for quit, or the new category
            try:
                result = int(result)
                podcast.category = categories[result-1].category_id
                break
            except ValueError:
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
        episodes = backend.get_episodes_from_feed(podcast.url)
        sql.insert_podcast(podcast, episodes)


def edit_existing_podcast():
    try:
        podcasts = sql.get_all_podcasts()
        podcast = print_out_menu_options(podcasts, 'name', False, None, True)
        if podcast is not None:
            enter_podcast_info(podcast)
            if podcast != None:
                episodes = backend.get_episodes_from_feed(podcast.url)
                sql.delete_episodes_by_podcast_id(podcast)
                sql.update_podcast2(podcast, episodes)
    except KeyboardInterrupt as e:
        sql.log(str(e))



def choose_episodes_to_download():
    try:
        os.system('clear')
        print('number 1 by name')
        print('number 2 by category')
        choice = input('choice: ')
        if choice == 'q':
            main_menu()
        choice = int(choice)
        if choice == 1:
            choose_episodes_to_download_by_name()
        elif choice == 2:
            choose_episode_to_download_by_category()
        else:
            main_menu()
    except ValueError:
        main_menu()
    except KeyboardInterrupt:
        main_menu()


def choose_episodes_to_download_by_name():
    podcasts = sql.get_podcasts_with_downloads_available()
    print_out_menu_options(podcasts, 'name', False, list_episodes, True)


def choose_episode_to_download_by_category():
    categories = sql.get_all_categories()
    choice = print_out_menu_options(
        categories, 'category', False, False, False)
    if choice is not None:
        podcasts = sql.get_all_podcasts_with_category(choice)
        print_out_menu_options(podcasts, 'name', False, list_episodes, True)


def list_episodes(podcast,mark_read=False):
    episodes = sql.get_episodes_with_downloads_available(podcast)
    if (len(episodes) > 0):
        print_out_menu_options(episodes, 'title', True,
                            add_to_download_queue, False)
        # horrible horrible hack - checks to see if any of the episodes were
        # added to the download queue. find all that were and mark the rest as 
        # read
        added_episodes = [value for value in download_queue if value in episodes]
        not_added_episodes = [value for value in episodes if value not in added_episodes]
        for ep in not_added_episodes:
            sql.update_episode_as_downloaded(ep)


def list_episodes_arch(podcast):
    episodes = sql.get_all_episodes(podcast)
    if episodes:
        print_out_menu_options(episodes, 'title', True,
                               add_to_download_queue, False)


    else:
        sql.log('Something went horribly wrong with gettin all the episodes')


def add_to_download_queue(episode):
    download_queue.append(episode)
    write_state_information()


def write_state_information():
    try:
        episode_ids = []
        for each in download_queue:
            episode_ids.append(each.episode_id)
        state = open(config.pickled_file_location, 'wb')
        pickle.dump(episode_ids, state)
    except Exception as e:
        sql.log(e)


def read_state_information():
    download_queue_local = []
    state = open(config.pickled_file_location, 'rb')
    episode_ids = pickle.load(state)
    for each in episode_ids:
        epi = sql.get_episode_by_id(each)
        if epi:
            download_queue_local.append(epi)
        else:
            sql.log("could not read episode with episode_id:{}".format(each))
    return download_queue_local


def start_downloads():
    download_queue_removed = []
    try:
        print('starting downloads...')
        total_queue_length = len(download_queue)
        for each in download_queue:
            each.percent = 0
        for i, each in enumerate(download_queue):
            try:
                filename = each.href.split('/')[-1]
                extension_start = filename.split('.')
                extension = extension_start[len(extension_start)-1]
                extension = extension.split('?', 1)[0]
                dl_location = ''
                podcast = sql.get_podcast_by_id2(each)
                filename2 = podcast.name.replace(
                    " ", "-").replace("/", "-").lower()
                if each.audio == 1:
                    dl_location = podcast.audio  # [0]['audio']
                else:
                    dl_location = podcast.video  # [0]['video']

                basename = filename2 + "-" + \
                    each.title.replace(" ", "-").lower()  # +"."+extension
                basename = (basename[:240]) if len(
                    basename) > 240 else basename
                basename += "-" + \
                    each.published.strftime("%Y%m%d") + "."+extension
                if hasattr(config, "dl_location_file_location"):
                    dl_location = config.dl_location_file_location
                else:
                    dl_location = config.download_pre_location + dl_location

                try:
                    # Adding download prefix to dl_location to address the difference of
                    # being in the docker container
                    with open(dl_location + '/' + basename, 'wb')as f:
                        r = requests.get(each.href, stream=True)
                        total_length = None
                        dl=0
                        try:
                            total_length = int(r.headers.get('content-length'))
                            for chunk in r.iter_content(1024):
                                dl += len(chunk)
                                f.write(chunk)
                                done = int(100 * dl / total_length)
                                download_queue[i].percent = done
                        except Exception as e:
                            f.write(r.content)
                        # dl = 0
                        # if total_length is None:  # no content length header
                        #     f.write(r.content)
                        # else:
                        #     for chunk in r.iter_content(1024):
                        #         dl += len(chunk)
                        #         f.write(chunk)
                        #         done = int(100 * dl / total_length)
                        #         download_queue[i].percent = done

                    updated = sql.update_episode_as_downloaded(each)
                    if updated:
                        print('saved {} of {} - {}'.format(i +
                                                           1, total_queue_length, basename))
                        download_queue_removed.append(each)
                        sql.log("downloaded {}".format(each))
                except FileNotFoundError as e:
                    string = "FileNotFoundError problem saving {}".format(
                        basename)
                    print(string)
                    sql.log(string)
                    sql.log(str(e))
                except ConnectionError as e:
                    string = "ConnectionError problem saving {}".format(
                        basename)
                    print(string)
                    sql.log(string)
                    sql.log(e)
                except OSError as e:
                    string = "OSError problem saving {}".format(basename)
                    print(string)
                    sql.log(string)
                    sql.log(e)
                except Exception as e:
                    string = "Exception problem saving {}".format(basename)
                    print(string)
                    sql.log(string)
                    sql.log(e)
            except Exception as e:
                string = "problem with Episode data"
                sql.log(e)

        for each in download_queue_removed:
            download_queue.remove(each)

        write_state_information()

        input('return to continue ')

    except KeyboardInterrupt:
        pass
        for each in download_queue_removed:
            download_queue.remove(each)


def rlinput(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


def print_out_menu_options(options, attribute, multi_choice, func, sort, archived=False):
    if len(options) == 0:
        print('Zero results')
        time.sleep(2)
        return None
    try:
        if sort:
            options.sort(key=lambda x: getattr(x, attribute))
        if len(options) < 2:
            multi_choice = False

        choices = []
        full = int(math.floor(len(options) / height))
        remainder = len(options) - (full * height)

        display_control = []
        counter = 0
        line_counter = 0
        temp = []
        if isinstance(options[0], Episode):
            for each in options:
                possible_length = float(len('number {} {}'.format("00000", getattr(each, attribute))))
                each.lines = int(math.ceil(possible_length/width))
            for itr,opt in enumerate(options):
                if line_counter + opt.lines >= height:
                    display_control.append(temp.copy())
                    temp.clear()
                    line_counter = 0
                    temp.append(itr)
                    line_counter += opt.lines
                else:
                    temp.append(itr)
                    line_counter += opt.lines
                # sql.log("{}:{}".format(itr,len(display_control)))
            display_control.append(temp)
                
        else:
            for each in range(full):
                temp = []
                for itr in range(height):
                    temp.append(counter)
                    counter += 1

                display_control.append(temp)
            temp = []
            for each in range(remainder):
                temp.append(counter)
                counter += 1

            display_control.append(temp)

        page_itr = 0

        while True:
            os.system('clear')
            if len(options) == 0:
                print('no results found')
            for each in display_control[page_itr]:
                try:
                    if isinstance(options[each], Podcast):
                        number = sql.get_number_of_available_episodes_by_podcast(
                            options[each], archived)
                    # This is put the number of available downloads after the podcast listing. Pasta!
                    # if hasattr(options[each], 'num'):
                        print('number {} {} - {}'.format(each + 1,
                                                        getattr(options[each], attribute), number))
                    else:
                        print('number {} {}'.format(
                            each + 1, getattr(options[each], attribute)))
                except Exception as e:
                    sql.log(e)
            result = input('choice ')
            if result == 'n':
                if page_itr < len(display_control) - 1:
                    page_itr += 1
            elif result == 'p':
                if page_itr > 0:
                    page_itr -= 1
            elif result == 'q':
                if len(choices) > 0:
                    return choices
                break
            elif result == 'c':
                if isinstance(options[0], Episode):
                    sql.update_episodes_as_viewed(options)
                    break

            elif result == 'a':
                try:
                    for each in options:
                        func(each)
                    break
                except Exception:
                    pass
            else:
                # this is looking for entries that are in the form 1-4 to represent
                # choices 1,2,3,4 - requested option
                # first separate out the 1-4 options whether they have spaces in betweeen
                # the numbers and dashes or not
                dashed_option_choices = re.findall(
                    r'[0-9]{1,2}\ ?\-\ ?[0-9]{1,2}', result)
                result = re.sub(r'[0-9]{1,2}\ ?\-\ ?[0-9]{1,2}', '', result)
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
                                func(options[item - 1])
                            elif multi_choice:
                                choices.append(options[item-1])
                            elif func:
                                func(options[item-1])
                            else:
                                return options[item-1]
                    except ValueError:
                        pass
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    width = int(subprocess.check_output(['tput', 'cols']))
    height = int(subprocess.check_output(['tput', 'lines'])) - 1


    sql = DatabaseAccessor(config.database_location)
    download_queue = read_state_information()
    backend = Backend(sql)


    main_menu()
