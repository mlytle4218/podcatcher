#!/usr/bin/env python3
import feedparser
import calendar
import csv
import datetime,time
from sql_alchemy_setup import Episode, Podcast


class Backend:

    def __init__(self, database_accessor):
        self.database_accessor = database_accessor


    def log(self,input):
        with open("test.txt", "a") as myfile:
            string=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            string=string+ ' - ' +input + '\n'
            myfile.write(string)


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


    def get_podcast_data_from_feed(self,url):
        f_parser = feedparser.parse(url)
        episode_list = []
        for entry in f_parser['entries']:
            episode = Episode()
            for sub_entry in entry:
                # log( sub_entry )
                if(sub_entry == 'title'):
                    episode.title = self.remove_tags(entry['title'])#.encode('utf-8')
                elif (sub_entry == 'summary'):
                    episode.summary =  self.remove_tags(entry['summary'])#.encode('utf-8')
                elif ( sub_entry == 'links' ):
                    for link in entry['links']:
                            if 'text' not in link['type']:

                                episode.href = link['href']
                                if link.has_key('length'):
                                    episode.length = link['length']
                                else: 
                                    episode.length = -1
                                
                                if 'audio' in link['type']:
                                    episode.audio = 1
                                else: 
                                    episode.audio = 0

                elif ( sub_entry == 'published'):
                    episode.published = datetime.datetime.strptime(entry['published'], '%a, %W %b %Y %H:%M:%S %z') 
            episode_list.append(episode)
        return episode_list


    def check_feed(self,input):
        d = feedparser.parse(input)
        if len(d.feed) == 0:
            return False
        else:
            return True







