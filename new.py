#!/usr/bin/env python3
import feedparser
import calendar
import csv
import datetime,time
# import self.database_accessor


# class LogIt:
#     def __init__(self, input):
#         self.input = input
#     def __call__(self):
#         log(str(self.input))

class Backend:

    def __init__(self, database_accessor):
        self.database_accessor = database_accessor


    def log(self,input):
        with open("test.txt", "a") as myfile:
            string=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            string=string+ ' - ' +input + '\n'
            myfile.write(string)
            



    # def get_new_entries(self,entries, last, audio, video):
    #     result_list = []
    #     for entry in entries:
    #         if calendar.timegm(entry.published_parsed) > int(last):
    #             temp_dict = {}
    #             temp_dict['id'] = entry.id
    #             temp_dict['title'] = entry.title
    #             temp_dict['published'] = entry.published
    #             temp_dict['summary'] = entry.summary
    #             temp_dict['audio_path'] = audio
    #             temp_dict['video_path'] = video
    #             temp_dict['last'] = last
    #             for link in entry.links:
    #                 if 'audio' in link.type or 'video' in link.type:
    #                     temp_dict['feed'] = {}
    #                     if 'audio' in link.type:
    #                         temp_dict['audio'] = link['href']
    #                     if 'video' in link.type:
    #                         temp_dict['video'] = link['href']
    #             result_list.append(temp_dict)
    #     return result_list

    # def get_data_from_csv(self,csv_file):
    #     with open(csv_file, 'r') as file:
    #         return list(csv.DictReader(file))

    # def get_feed_data_from_csv(self,csv_file):
    #     feed_dict={}
    #     csv_dict = self.get_data_from_csv(csv_file)
    #     # print csv_dict
    #     for row in csv_dict:
    #         NewsFeed = feedparser.parse(row['feed'])
    #         self.log(str(row))
    #         title = NewsFeed['feed']['title']#.replace(' ','_').lower()
    #         feed_dict[title] = self.get_new_entries(NewsFeed['entries'],row['last'],row['audio'],row['video'])

    #     return feed_dict

    # def append_to_csv(self,input_dict, csv_file):
    #     with open(csv_file, 'a') as file:
    #         writer = csv.writer(file)
    #         writer.writerow([input_dict['name'],input_dict['feed'],input_dict['audio'], input_dict['video'],input_dict['last'] ])


    def remove_tags(self,html_string):
        html_string = html_string.replace("'", "")
        html_string = html_string.replace('"', '')
        html_string = html_string.lstrip("\'")
        html_string = html_string.rstrip("\'")
        html_string = html_string.replace('<p><br /> ','')
        html_string = html_string.replace('<p> ','\n')
        html_string = html_string.replace('<br /> ','\n')
        html_string = ''.join([i if ord(i) < 128 else '' for i in html_string])
        return html_string

    # def start_download(self,feed_file):
    #     feed_dict = self.get_feed_data_from_csv(feed_file)
    #     for key in feed_dict.keys():
    #         audio_path=''
    #         video_path=''
    #         last = 0
    #         with open(feed_file, 'r+') as file:
    #             dictReader = csv.DictReader(file)
    #             for row in dictReader:
    #                 self.log( row['name'] )
    #                 if row['name'] == key:
    #                     audio_path = row['audio']
    #                     video_path = row['video']
    #                     last = row['last']
    #             for feed in feed_dict[key]:
    #                 if 'audio' in feed:
    #                     self.log('download ' + feed['audio'] + " to " + audio_path)
    #                 elif 'video' in feed:
    #                     self.log('download ' + feed['video'] + " to " + video_path)

    #     #     for feed in feed_dict[key]:
    #     #         print(feed['id'])
    #     #         print(feed['title'])
    #     #         print( remove_tags(feed['summary']))
    #     #         if 'audio' in feed:
    #     #             print(feed['audio'])
    #     #         elif 'video' in feed:
    #     #             print(feed['video'])
    #     #         print("")
    #     #     print("")
    #     return 0


    def add_new_podcast(self,input):
        input['podcast_id'] = self.database_accessor.insert_podcast(input)
        episodes = self.get_podcast_data_from_feed(input['url'])
        self.database_accessor.insert_episodes(input['podcast_id'], episodes)
        return input

    def update_podcast(self,input):
        id = self.database_accessor.update_podcast(input)
        return id

    def update_episode_as_downloaded(self,episode):
        id = self.database_accessor.update_episode_as_downloaded_by_id(episode['episode_id']) 
        # log( 'new update downloaded ' + str( id ) )
        return id

    def remove_podcast(self,input):
        id = self.database_accessor.delete_podcast(input)
        return id

    def get_download_location_from_podcast_id(self,podcast_id):
        podcast = self.database_accessor.select_podcast_from_id(podcast_id)
        return podcast


# https://feeds.fireside.fm/thebulwark/rss


    def get_podcast_data_from_feed(self,url):
        f_parser = feedparser.parse(url)
        episode_list = []
        for entry in f_parser['entries']:
            episode = {}
            for sub_entry in entry:
                # log( sub_entry )
                if(sub_entry == 'title'):
                    episode['title'] = self.remove_tags(entry['title'])#.encode('utf-8')
                elif (sub_entry == 'summary'):
                    episode['summary'] =  self.remove_tags(entry['summary'])#.encode('utf-8')
                elif ( sub_entry == 'links' ):
                    # see if it has a lenght and add it or add -1
                    # if entry['links'][0].has_key('length'):
                    #     episode['length'] = entry['links'][0]['length']
                    # else:
                    #     episode['length'] = -1

                    # add actual href    
                    # episode['href'] = entry['links'][0]['href']
                    for link in entry['links']:
                            if 'text' not in link['type']:

                                episode['href'] = link['href']
                                if link.has_key('length'):
                                    episode['length'] = link['length']
                                else: 
                                    episode['length'] = -1
                                
                                if 'audio' in link['type']:
                                    episode['audio'] = 1
                                else: 
                                    episode['audio'] = 0

                    # if it has type and that contains 'audio' in it return 1 else 0
                    # if entry['links'][0].has_key('type'):
                    #     if 'audio' in entry['links'][0]['type']:
                    #         episode['audio'] = 1
                    #     else:
                    #         episode['audio'] = 0

                elif ( sub_entry == 'published'):
                    episode['published'] = datetime.datetime.strptime(entry['published'], '%a, %W %b %Y %H:%M:%S %z') 
                episode['downloaded'] = 0
            episode_list.append(episode)
        return episode_list


    def get_podcasts_that_have_downloads_available(self):
        return self.database_accessor.select_podcasts_that_have_downloads_available()

    def get_episodes_that_have_downloads_available_from_podcast_id(self,podcast):
        return self.database_accessor.select_episodes_that_have_downlaods_available_by_podcast_id(podcast)


    def get_episodes_by_podcast_id(self,id):
        return self.database_accessor.select_episodes_from_podcast_id(id)


    def check_feed(self,input):
        d = feedparser.parse(input)
        if len(d.feed) == 0:
            return False
        else:
            return True

    def find_new_podcasts(self,name):
        feed_url,id = self.database_accessor.select_feed_from_name(name)
        feed_episodes = self.get_podcast_data_from_feed(feed_url)
        db_episodes = self.database_accessor.select_episodes_from_podcast_id(id)

        # 1 is title
        # 3 is published
        # 5 is length

        indices = []
        for db_ep in db_episodes:
            for idx,feed in enumerate(feed_episodes):
                try: 
                    if (db_ep[3] == feed['published'] and db_ep[3] == feed['published'] and db_ep[5] == int(feed['length'])):
                        indices.append(idx)
                        break
                except Exception as e:
                    print(e)


        for index in sorted(indices, reverse=True):
            del feed_episodes[index]

        return self.database_accessor.insert_episodes(name, feed_episodes)

    def get_podcast_dict(self):
        result = { 'name':'','url':'','audio':'','video':''}
        return result
        
    def get_podcasts(self):
        return self.database_accessor.select_all_podcasts()


    # feed_dict = get_feed_data_from_csv('feeds.csv')
    # self.database_accessor.start_new_database()

    # here = {'name':'bulwark','url':'https://podcast.thebulwark.com/rss,/home/marc/Desktop/podcatcher/bulwark','audio':'/home/marc/Desktop/podcatcher/bulwark','video':'/home/marc/Desktop/podcatcher/bulwark'}
    # here2 = {'name':'starthere','url':'http://feeds.feedburner.com/abcradio/starthere','audio':'/home/marc/Desktop/podcatcher/bulwark','video':'/home/marc/Desktop/podcatcher/bulwark'}
    # print(self.database_accessor.insert_podcast(here))
    # self.database_accessor.insert_podcast(here2)



    # print(find_new_podcast('starthere'))
    # self.database_accessor.select_all_podcasts()






