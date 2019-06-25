#!/usr/bin/env python3
import sqlite3
import itertools
import datetime
import time
from sqlalchemy import  create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey

    # database = 'pc_database.db'


class DatabaseAccessor:
    def __init__(self,database):
        self.database = database
        self.engine = create_engine('sqlite:///%s' % database, echo = True)
        self.meta = MetaData()
        self.conn = self.engine.connect()

        self.podcasts = Table(
            'podcasts', self.meta,
            Column('podcast_id',Integer, primary_key = True),
            Column('name',String),
            Column('url',String),
            Column('audio',String),
            Column('video',String),
        )

        self.episodes = Table(
            'episodes', self.meta,
            Column('episode_id', Integer, primary_key = True),
            Column('title', String),
            Column('url', String),
            Column('published', DateTime),
            Column('summary', String),
            Column('length', Integer),
            Column('audio', Integer),
            Column('downloaded', Integer),
            Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id'))
        )

        self.meta.create_all(self.engine)



    # database = 'pc_database.db'

    def log(self,input):
        with open("test.txt", "a") as myfile:
            string=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            string=string+ ' - ' +input + '\n'
            myfile.write(string)

    # class LogIt:
    #     def __init__(self, input):
    #         self.input = input
    #     def __call__(self):
    #     self.log(str(self.input))

    def trial(self):
        return 'worked'

    def start_new_database(self):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute("""CREATE TABLE podcasts ( 
            podcast_id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL, 
            url TEXT NOT NULL,
            audio TEXT NOT NULL,
            video TEXT NOT NULL)""")
        c.execute("""CREATE TABLE episodes ( 
            episode_id INTEGER PRIMARY KEY, 
            title TEXT NOT NULL, 
            url TEXT NOT NULL,
            published DATE NOT NULL,
            summary TEXT NOT NULL,
            length INTEGER NOT NULL,
            audio INTEGER NOT NULL,
            downloaded INTEGER DEFAULT 0,
            podcast_id INTEGER NOT NULL,
            FOREIGN KEY(podcast_id) REFERENCES podcasts(podcast_id))""")
        conn.commit()
        conn.close()


    def connect_db(self):
        conn = sqlite3.connect(self.database)
        return conn

    def close_db(self,conn):
        conn.close()

    def commit_db(self,conn):
        conn.commit()
        conn.close
        
    def insert_podcast(self,input):
        conn = self.connect_db()
        c = conn.cursor()
        c.execute("INSERT INTO podcasts (name, url, audio, video) VALUES ('{nm}', '{ur}', '{au}','{vi}')".format(
            nm=input['name'],ur=input['url'],au=input['audio'],vi=input['video']
            ))
        result = c.lastrowid
        self.commit_db(conn)
        return result
        
    def insert_podcast2(self,podcast,episodes):
        result = self.conn.execute(self.podcasts.insert(podcast))

        for each in episodes:
            each['podcast_id'] = result.inserted_primary_key[0]

        self.conn.execute(self.episodes.insert(None), episodes)


    def delete_podcast(self,podcast):
        conn = self.connect_db()
        c = conn.cursor()
        command =  "DELETE FROM episodes WHERE podcast_id = '{id}'".format(id=podcast['podcast_id'])
        self.log(command)
        c.execute( command )
        conn.commit()
        command =  "DELETE FROM podcasts WHERE podcast_id = '{id}'".format(id=podcast['podcast_id'])
        c.execute( command )
        self.commit_db(conn)
        return 1




    def update_podcast(self,input):
        conn = self.connect_db()
        c = conn.cursor()
        command = """UPDATE podcasts SET 
                name = '{name}',
                url = '{url}',
                audio = '{audio}',
                video = '{video}'
            WHERE 
                podcast_id = '{podcast_id}';
        """.format(name=input['name'],
            url=input['url'],
            audio=input['audio'],
            video=input['video'],
            podcast_id=input['podcast_id'])
        c.execute(command)
        self.commit_db(conn)
        return c.lastrowid

    def update_episode_as_downloaded_by_id(self,episode_id):
        conn = self.connect_db()
        c = conn.cursor()
        command = """UPDATE episodes SET downloaded = '{}' WHERE episode_id = '{}';""".format(
            1,
            episode_id
        )
        temp_cursor = c.execute(command)
        result = temp_cursor.rowcount
        self.commit_db(conn)
        return result

    def insert_episodes(self,podcast_id, episodes):
        conn = self.connect_db()
        c = conn.cursor()
        # podcast_id = select_podcast_id(c, podcast)
        for episode in episodes:
            # print(episode)
            sub_select  = """INSERT INTO episodes (title, 
                url, 
                published, 
                length, 
                audio,
                summary,
                podcast_id) VALUES(
                    '{title}',
                    '{url}',
                    '{published}',
                    '{length}',
                    '{audio}',
                    '{summary}',
                    '{podcast_id}')""".format(
                        title = episode['title'],
                        url = episode['href'],
                        published = episode['published'],
                        length = episode['length'],
                        audio = episode['audio'],
                        summary = episode['summary'],

                        podcast_id = podcast_id
                    )
            c.execute(sub_select)
        self.commit_db(conn)
        return podcast_id

    def select_episodes_from_podcast_id(self,id):
        conn = self.connect_db()
        c = conn.cursor()
        command = """SELECT * FROM episodes WHERE podcast_id = '{podcast_id}'""".format(podcast_id=id)
        self.log( command )
        c.execute( command )
        results = self.make_cursor_response_into_dict(c)
        return results

    def select_podcast_id(self,c, podcast_name):
        podcast_id = c.execute("SELECT podcast_id FROM podcasts WHERE name = '{}';".format(podcast_name)).fetchall()[0][0]
        return podcast_id

    def select_all_podcasts(self):
        conn = self.connect_db()
        c = conn.cursor()
        c.execute("SELECT * from podcasts")
        column_names = [col[0] for col in c.description]
        results = [dict(zip(column_names, row))  
            for row in c.fetchall()]
        self.close_db(conn)
        return results

    def select_podcast_from_id(self,id):
        conn = self.connect_db()
        c = conn.cursor()
        c.execute("""SELECT * FROM podcasts WHERE podcast_id = '{}';""".format(id))
        results = self.make_cursor_response_into_dict(c)
        self.close_db(conn)
        return results


    def select_feed_from_name(self,name):
        conn = self.connect_db()
        c = conn.cursor()
        result = c.execute("SELECT url,podcast_id FROM podcasts where name = '{}'".format(name)).fetchall()[0]
        self.close_db(conn)
        return result[0],result[1]


    def select_podcasts_that_have_downloads_available(self):
        conn = self.connect_db()
        c = conn.cursor()
        command = """SELECT * FROM podcasts WHERE (SELECT podcast_id from episodes where downloaded = '0');"""
        c.execute( command )
        results = self.make_cursor_response_into_dict(c)
        self.close_db(conn)
        return results

    def select_episodes_that_have_downlaods_available_by_podcast_id(self,podcast):
        conn = self.connect_db()
        c = conn.cursor()
        c.execute("""SELECT * FROM episodes WHERE podcast_id = '{}' and downloaded = '0';""".format(podcast['podcast_id']))
        results = self.make_cursor_response_into_dict(c)
        self.close_db(conn)
        return results



    def make_cursor_response_into_dict(self,cursor):
        column_names = [col[0] for col in cursor.description]
        results = [dict(zip(column_names, row))  
            for row in cursor.fetchall()]
        
        return results



# da = DatabaseAccessor('pc_database2.db')

# podcast = {}
# podcast['name'] = 'name'
# podcast['url'] = 'url'
# podcast['audio'] = 'audio'
# podcast['video'] = 'video'


# result = da.conn.execute(da.podcasts.insert(podcast))


# episodes = []
# for i in range(10):
#     episode = {}
#     episode['title'] = 'title{}'.format(i)
#     episode['url'] = 'url{}'.format(i)
#     # episode['published'] = 'published{}'.format(i)
#     episode['published'] = datetime.datetime.now()
#     episode['summary'] = 'summary{}'.format(i)
#     episode['length'] = i
#     episode['audio'] = i
#     episode['downloaded'] = i
#     episode['podcast_id'] = result.inserted_primary_key[0]
#     episodes.append(episode)

# result2 = da.conn.execute(da.episodes.insert(None), episodes)
