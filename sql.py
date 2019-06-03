#!/usr/bin/env python
import sqlite3
import itertools
import datetime
import time

database = 'pc_database.db'



def log(input):
    with open("test.txt", "a") as myfile:
        string=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        string=string+ ' - ' +input + '\n'
        myfile.write(string)

class LogIt:
    def __init__(self, input):
        self.input = input
    def __call__(self):
       log(str(self.input))

def trial():
    return 'worked'

def start_new_database():
    conn = sqlite3.connect(database)
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


def connect_db():
    conn = sqlite3.connect(database)
    return conn

def close_db(conn):
    conn.close()

def commit_db(conn):
    conn.commit()
    conn.close
    
def insert_podcast(input):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO podcasts (name, url, audio, video) VALUES ('{nm}', '{ur}', '{au}','{vi}')".format(
        nm=input['name'],ur=input['url'],au=input['audio'],vi=input['video']
        ))
    result = c.lastrowid
    commit_db(conn)
    return result

def delete_podcast(podcast_id):
    conn = connect_db()
    c = conn.cursor()
    command =  "DELETE FROM episodes WHERE podcast_id = '{id}'".format(id=podcast_id)
    c.execute( command )
    conn.commit()
    command =  "DELETE FROM podcasts WHERE podcast_id = '{id}'".format(id=podcast_id)
    c.execute( command )
    commit_db(conn)
    return 1




def update_podcast(input):
    conn = connect_db()
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
    commit_db(conn)
    return c.lastrowid

def insert_episodes(podcast_id, episodes):
    conn = connect_db()
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
    commit_db(conn)
    return podcast_id

def select_episodes_from_podcast_id(id):
    conn = connect_db()
    c = conn.cursor()
    command = """SELECT * FROM episodes WHERE podcast_id = '{podcast_id}'""".format(podcast_id=id)
    log( command )
    c.execute( command )
    results = make_cursor_response_into_dict(c)
    return results

def select_podcast_id(c, podcast_name):
    podcast_id = c.execute("SELECT podcast_id FROM podcasts WHERE name = '{}';".format(podcast_name)).fetchall()[0][0]
    return podcast_id

def select_all_podcasts():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * from podcasts")
    column_names = [col[0] for col in c.description]
    results = [dict(itertools.izip(column_names, row))  
        for row in c.fetchall()]
    close_db(conn)
    return results


def select_feed_from_name(name):
    conn = connect_db()
    c = conn.cursor()
    result = c.execute("SELECT url,podcast_id FROM podcasts where name = '{}'".format(name)).fetchall()[0]
    close_db(conn)
    return result[0],result[1]


def select_podcasts_that_have_downloads_available():
    conn = connect_db()
    c = conn.cursor()
    command = """SELECT * FROM podcasts WHERE (SELECT podcast_id from episodes where downloaded = '0');"""
    c.execute( command )
    results = make_cursor_response_into_dict(c)
    close_db(conn)
    return results

def make_cursor_response_into_dict(cursor):
    column_names = [col[0] for col in cursor.description]
    results = [dict(itertools.izip(column_names, row))  
        for row in cursor.fetchall()]
    
    return results

