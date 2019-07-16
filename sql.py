#!/usr/bin/env python3
import sqlite3
import itertools
import datetime
import time
from sqlalchemy import  create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sql_alchemy_setup import Podcast, Episode, Base

    # database = 'pc_database.db'








class DatabaseAccessor:
    def __init__(self,database):
        # self.database = database
        data_base = "sqlite:///{}".format(database)
        # self.log( str( data_base ) )
        self.engine = create_engine(data_base)
        # self.engine = create_engine('sqlite:///%s' % database)
        # self.meta = MetaData()
        # self.conn = self.engine.connect()
        
        # self.engine = create_engine('sqlite:///sqlalchemy_example.db')

        self.Base = declarative_base()
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        self.Base.metadata.bind = self.engine

        self.Base.metadata.create_all(self.engine)
        
        self.DBSession = sessionmaker(bind=self.engine)
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
        self.session = self.DBSession()
        
        # # Insert a Person in the person table
        # new_person = Person(name='new person')
        # session.add(new_person)
        # session.commit()
        
        # # Insert an Address in the address table
        # new_address = Address(post_code='00000', person=new_person)
        # session.add(new_address)
        # session.commit()

 

    def log(self,input):
        with open("test.txt", "a") as myfile:
            string=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            string=string+ ' - ' +input + '\n'
            myfile.write(string)

    def insert_episodes(self, episodes):
        for each in episodes:
            self.session.add(
                Episode(
                    each.title,
                    each.published,
                    each.summary,
                    each.length,
                    each.audio,
                    each.podcast_id,
                    each.href
                )
            )
        self.session.commit()
        
    def insert_podcast2(self,podcast,episodes):
        self.session.add(podcast)
        self.session.commit()
        self.log('got here')
        for each in episodes:
            each.podcast_id = podcast.podcast_id
            self.session.add(Episode(each.title, each.published, each.summary, each.length,each.audio,each.podcast_id, each.href ))

        self.session.commit()

    def get_first_podcast(self):
        return self.session.query(Podcast).first()

    def get_episodes_by_podcast_id(self,podcast):
        episodes =  self.session.query(Episode).filter(Episode.podcast_id == podcast.podcast_id).all()
        return self.result_proxy_to_dict(episodes)


    def update_all_episodes(self):
        episodes = self.session.query(Episode).all()
        return episodes

    def get_all_podcasts(self):
        podcasts = self.session.query(Podcast).all()
        return self.result_proxy_to_dict( podcasts )

    def result_proxy_to_dict(self,input):
        results = []
        for each in input:
            results.append( each.__dict__ )
        # return results
        return input


    def delete_podcast2(self,podcast):
        self.session.query(Episode).filter(Episode.podcast_id == podcast.podcast_id ).delete()
        self.session.commit()
        self.session.query(Podcast).filter(Podcast.podcast_id == podcast.podcast_id).delete()
        self.session.commit()

    def delete_episodes_by_podcast_id(self, podcast):
        self.session.query(Episode).filter(Episode.podcast_id == podcast.podcast_id ).delete()
        self.session.commit()

    def update_podcast2(self,podcast,episodes):
        for each in episodes:
            each.podcast_id = podcast.podcast_id
            self.session.add(each)

        self.session.commit()

    def get_podcasts_with_downloads_available(self):
        podcasts =  self.session.query(Podcast).join(Episode).filter(Episode.downloaded == 0).all()
        return self.result_proxy_to_dict( podcasts)

    def get_episodes_with_downloads_available(self, podcast):
        episodes = self.session.query(Episode).filter(Episode.podcast_id == podcast.podcast_id).filter(Episode.downloaded ==0).all()
        return self.result_proxy_to_dict( episodes )

    def get_podcast_by_id2(self,episode):
        podcast = self.session.query(Podcast).filter(Podcast.podcast_id == episode.podcast_id).one()
        return podcast
        # return self.result_proxy_to_dict( podcast )
    
    def update_episode_as_downloaded(self,episode):
        epi_temp = self.session.query(Episode).filter(Episode.episode_id == episode.episode_id).one()
        epi_temp.downloaded = 1
        self.session.commit()