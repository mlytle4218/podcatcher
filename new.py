#!/usr/bin/env python3
import feedparser
import calendar
import csv
import datetime,time
from sql_alchemy_setup import Episode, Podcast
import re
import config
import sys
import requests


class Backend:

    def __init__(self, database_accessor):
        self.database_accessor = database_accessor


    def log(self,input):
        with open(config.log_location, "a") as myfile:
            string=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            string=string+ ' - ' +input + '\n'
            myfile.write(string)


    def remove_tags(self,html_string):
        html_string = html_string.replace('<p><br /> ','')
        html_string = html_string.replace('<p> ','\n')
        html_string = html_string.replace('<br /> ','\n')
        html_string = html_string.replace('/','-')
        html_string = ''.join([i if ord(i) < 128 else '' for i in html_string])
        whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        html_string = ''.join(filter(whitelist.__contains__, html_string))
        html_string = html_string.replace(' ','-').lower()
        return html_string

    def get_episodes_from_feed(self,url):
        try:
            resp = requests.get(url, timeout=10.0)
        except requests.ReadTimeout:
            self.log(str("ReadTimeout for {}".format(url)))
            return None
        except requests.ConnectTimeout as e:
            self.log('ConnectTimeout for {}'.format(url))
            self.log(str(e))
            return None

        except Exception as e:
            self.log('Unknown Exception for {}'.format(url))
            self.log(str(e))
            return None


            
        f_parser = feedparser.parse(resp.content)
        episode_list = []
        for entry in f_parser['entries']:
            result = self.get_episode_from_feed_parser(entry)
            if result:
                episode_list.append(result)
        return episode_list

    def get_episode_from_feed_parser(self, entry):
        try:
            if 'links' in entry:
                episode = Episode()
                episode.title = self.remove_tags(entry.title)
                episode.summary = self.remove_tags(entry.summary)
                episode.href = None
                episode.audio = -1
                for link in entry.links:
                    if 'audio' in link.type:
                        episode.href = link.href
                        episode.audio = 1
                    if 'video' in link.type:
                        episode.href = link.href
                        episode.audio = 0
                episode.length = -1
                if 'itunes_duration' in entry:
                    episode.length = entry.itunes_duration
                try: 
                    #using regex to find only what we want - getting rid of any extras that are causing a commotion
                    p = re.compile('^[a-zA-Z]{3}, [0-9]{2} [a-zA-Z]{3} [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}')
                    result = p.findall(entry['published'])
                    if len(result) > 0:
                        episode.published = datetime.datetime.strptime(result[0], '%a, %W %b %Y %H:%M:%S')
                    else:
                        return None
                except Exception as e:
                    self.log('published')
                    self.log( str( e ) )

                return episode
        except Exception as e:
            self.log('Error parsing entry {}'.format(str(entry)))
            self.log(str(e))
            return None


    def check_feed(self,input):
        d = feedparser.parse(input)
        if len(d.feed) == 0:
            return False
        else:
            return True



if __name__ == "__main__":
    bk = Backend(config.database_location)
    results = bk.get_episodes_from_feed(sys.argv[1])
    for each in results:
        print( each )



