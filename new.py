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
        # html_string = html_string.replace("'", "")
        # html_string = html_string.replace('"', '')
        # html_string = html_string.lstrip("\'")
        # html_string = html_string.rstrip("\'")
        # html_string = html_string.replace('<p><br /> ','')
        # html_string = html_string.replace('<p> ','\n')
        # html_string = html_string.replace('<br /> ','\n')
        # html_string = html_string.replace('/','-')
        # html_string = ''.join([i if ord(i) < 128 else '' for i in html_string])
        return html_string


    def get_podcast_data_from_feed2(self,url):
        self.log('in get_podcast_data_from_feed')
        try:
            resp = requests.get(url, timeout=20.0)
        except requests.ReadTimeout:
            self.log(str("Timeout when reading RSS %s", url))
            return None
        except requests.ConnectTimeout as e:
            self.log(str(e))
            return None
            
        f_parser = feedparser.parse(resp.content)
        episode_list = []
        for entry in f_parser['entries']:
            episode = Episode()
            for sub_entry in entry:
                self.log("in sub_entry for {}".format(entry))
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
                    # print(entry['published'])
                    try: 
                        if 'CDT'  in entry['published']:
                            entry['published'] = re.sub('CDT', '', entry['published']).strip()
                            episode.published = datetime.datetime.strptime(entry['published'], '%a, %W %b %Y %H:%M:%S')
                        elif 'GMT' in entry['published']:
                            entry['published'] = re.sub('GMT', '', entry['published']).strip()
                            episode.published = datetime.datetime.strptime(entry['published'], '%a, %W %b %Y %H:%M:%S')

                        else:
                            episode.published = datetime.datetime.strptime(entry['published'], '%a, %W %b %Y %H:%M:%S %z')
                    except Exception as e:
                        self.log('published')
                        self.log( str( e ) )
                elif ( sub_entry == 'pubDate'):
                    try: 
                        if 'CDT'  in entry['pubDate']:
                            entry['pubDate'] = re.sub('CDT', '', entry['pubDate']).strip()
                            episode.published = datetime.datetime.strptime(entry['pubDate'], '%a, %W %b %Y %H:%M:%S')
                        else:
                            episode.published = datetime.datetime.strptime(entry['pubDate'], '%a, %W %b %Y %H:%M:%S %z')
                    except Exception as e:
                        self.log('pubDate')
                        self.log( str( e ) )
            episode_list.append(episode)
        return episode_list

    def get_podcast_data_from_feed(self,url):
        try:
            resp = requests.get(url, timeout=10.0)
        except requests.ReadTimeout:
            self.log(str("ReadTimeout for {}".format(url)))
            return None
        except requests.ConnectTimeout as e:
            self.log('ConnectTimeout for {}'.format(url))
            self.log(str(e))
        except Exception as e:
            self.log('Unknown Exception for {}'.format(url))
            self.log(str(e))


            
        f_parser = feedparser.parse(resp.content)
        episode_list = []
        for entry in f_parser['entries']:
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
                        if 'CDT'  in entry.published:
                            entry.published = re.sub('CDT', '', entry.published).strip()
                            episode.published = datetime.datetime.strptime(entry.published, '%a, %W %b %Y %H:%M:%S')
                        elif 'GMT' in entry.published:
                            entry.published = re.sub('GMT', '', entry.published).strip()
                            episode.published = datetime.datetime.strptime(entry.published, '%a, %W %b %Y %H:%M:%S')

                        else:
                            episode.published = datetime.datetime.strptime(entry.published, '%a, %W %b %Y %H:%M:%S %z')
                    except Exception as e:
                        self.log('published')
                        self.log( str( e ) )

                    episode_list.append(episode)
            except Exception as e:
                self.log('Error parsing entry {}'.format(str(entry)))
                self.log(str(e))
        return episode_list


    def check_feed(self,input):
        d = feedparser.parse(input)
        if len(d.feed) == 0:
            return False
        else:
            return True




# bk = Backend(config.database_location)
# results = bk.get_podcast_data_from_feed(sys.argv[1])
# for each in results:
#     print( each )



