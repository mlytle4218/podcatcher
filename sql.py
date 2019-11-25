#!/usr/bin/env python3
import sqlite3
import itertools
import datetime
import time
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sql_alchemy_setup import Podcast, Episode, Category, Base
import config

from new import Backend

# database = 'pc_database.db'


class DatabaseAccessor:
    def __init__(self, database):
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

    def log(self, input):
        with open(config.log_location, "a") as myfile:
            string = datetime.datetime.fromtimestamp(
                time.time()).strftime('%Y-%m-%d %H:%M:%S')
            string = string + ' - ' + str(input) + '\n'
            myfile.write(string)


    def get_number_of_available_episodes_by_podcast(self,podcast, archived=False):
        try:
            if archived:
                return self.session.query(Episode).filter(Episode.podcast_id == podcast.podcast_id).count()
            else:
                return self.session.query(Episode).filter(Episode.podcast_id == podcast.podcast_id).filter(Episode.veiwed == 0).filter(Episode.downloaded==0).count()
        except Exception:
            return 0


    def add_new_category(self, category):
        existing_cat = self.session.query(Category).filter(
            Category.category == category.category).all()
        if (len(existing_cat)) == 0:
            try:
                # temp_cat = Category(category)
                # self.session.add(temp_cat)
                self.session.add(category)
                self.session.commit()
                return True
            except Exception:
                return False
        # this is not good - find a better way
        return True

    def get_all_categories(self):
        categories = self.session.query(Category).all()
        return categories



    def update_episodes_as_viewed(self, episodes):
        if episodes is not None:
            for episode in episodes:
                try:
                    result = self.session.query(
                        Episode).get(episode.episode_id)
                    result.veiwed = 1
                    self.session.commit()
                except Exception as e:
                    self.log("update_episodes_as_viewed for {}".format(episode))
                    self.log(str(e))

    def update_episodes_fix(self, episodes, podcast):
        if episodes is not None:
            for each in episodes:
                try:
                    result = self.session.query(Episode).filter(Episode.title == each.title).filter(
                        Episode.published == each.published).first()
                    if result is None:
                        result = self.insert_single_episode(each)
                    else:
                        result.audio = each.audio
                        result.href = each.href
                        self.session.commit()
                except Exception as e:
                    self.log(str(e))
        else:
            return False

    def insert_single_episode(self, episode):
        try:
            self.session.add(
                Episode(
                    episode.title,
                    episode.published,
                    episode.summary,
                    episode.length,
                    episode.audio,
                    episode.podcast_id,
                    episode.href
                )
            )
            self.session.commit()
            return True
        except Exception as e:
            self.log(str(e))
            return False

    def insert_episodes(self, episodes):
        for each in episodes:
            return self.insert_single_episode(each)

    def insert_podcast(self, podcast, episodes):
        try:
            self.session.add(podcast)
            self.session.commit()
            for each in episodes:
                each.podcast_id = podcast.podcast_id
                self.session.add(
                    Episode(
                        each.title,
                        each.published,
                        each.summary,
                        each.length,
                        each.audio,
                        each.podcast_id,
                        each.href)
                )

            self.session.commit()
            return True
        except Exception as e:
            self.log(str(e))
            return False

    def get_first_podcast(self):
        return self.session.query(Podcast).first()

    def get_episodes_by_podcast_id(self, podcast):
        episodes = self.session.query(Episode).filter(
            Episode.podcast_id == podcast.podcast_id).all()
        # return self.result_proxy_to_dict(episodes)
        return episodes
    
    def get_all_episodes(self, podcast):
        try:
            episodes = self.session.query(Episode).filter(Episode.podcast_id == podcast.podcast_id).all()
            return episodes
        except Exception as e:
            self.log(str(e))
            return None

    def get_episode_by_id(self, id):
        try:
            episode = self.session.query(Episode).filter(
                Episode.episode_id == id).one()
            return episode
        except Exception as e:
            self.log(str(e))
            return None

    # def update_all_episodes(self):
    #     episodes = self.session.query(Episode).all()
    #     return episodes

    

    def get_all_podcasts(self):
        # podcasts = self.session.query(Podcast).all()
        # return self.result_proxy_to_dict(podcasts)
        return self.session.query(Podcast).all()

    def result_proxy_to_dict(self, input):
        # results = []
        # for each in input:
        #     results.append(each.__dict__)
        # return results
        return input

    def delete_podcast2(self, podcast):
        try:
            self.session.query(Episode).filter(
                Episode.podcast_id == podcast.podcast_id).delete()
            self.session.commit()
            self.session.query(Podcast).filter(
                Podcast.podcast_id == podcast.podcast_id).delete()
            self.session.commit()
            return True
        except Exception as e:
            self.log(str(e))
            return False

    def delete_episode(self, episode):
        try:
            self.session.query(Episode).filter(
                Episode.episode_id == episode.episode_id).delete()
            self.session.commit()
            return True
        except Exception as e:
            self.log('delete_episode')
            self.log(episode)
            self.log(str(e))
            return False

    def add_episode(self, episode):
        try:
            self.session.add(episode)
            self.session.commit()
            return True
        except Exception as e:
            self.log('add_episode')
            self.log(episode)
            self.log(str(e))
            return False

    def delete_episodes_by_podcast_id(self, podcast):
        try:
            self.session.query(Episode).filter(
                Episode.podcast_id == podcast.podcast_id).delete()
            self.session.commit()
            return True
        except Exception:
            return False

    def update_podcast2(self, podcast, episodes):
        try:
            for each in episodes:
                each.podcast_id = podcast.podcast_id
                self.session.add(each)

            self.session.commit()
            return True
        except Exception as e:
            self.log(str(e))
            return False



    def get_episodes_with_downloads_available(self, podcast):
        episodes = self.session.query(Episode).filter(
            Episode.podcast_id == podcast.podcast_id).filter(Episode.downloaded == 0).filter(Episode.veiwed == 0).all()
        # return self.result_proxy_to_dict(episodes)
        return episodes

    def get_podcasts_with_downloads_available(self):
        results = []
        podcasts = self.session.query(Podcast).join(
            Episode).filter(Episode.downloaded == 0).all()
        for podcast in podcasts:
            try:
                rows = self.session.query(Episode).filter(
                    Episode.podcast_id == podcast.podcast_id).filter(Episode.veiwed == 0).filter(Episode.downloaded == 0).count()
                podcast.num = rows
                if podcast.num > 0:
                    results.append(podcast)
            except Exception as e:
                self.log(str(e))
                podcast.num = 0
        # return self.result_proxy_to_dict(podcasts)
        return results


    def get_all_podcasts_with_category(self, category):
        results = []
        podcasts = self.session.query(Podcast).filter(
            Podcast.category == category.category_id).all()
        for podcast in podcasts:
            try:
                rows = self.session.query(Episode).filter(
                    Episode.podcast_id == podcast.podcast_id).filter(Episode.veiwed == 0).filter(Episode.downloaded == 0).count()
                podcast.num = rows
                if podcast.num > 0:
                    results.append(podcast)
                    self.log(podcast.num)
            except Exception as e:
                self.log(str(e))
                podcast.num = 0
        return results

    def get_podcast_by_id2(self, episode):
        podcast = self.session.query(Podcast).filter(
            Podcast.podcast_id == episode.podcast_id).one()
        return podcast
        # return self.result_proxy_to_dict( podcast )

    def update_episode_as_downloaded(self, episode):
        try:
            epi_temp = self.session.query(Episode).filter(
                Episode.episode_id == episode.episode_id).one()
            epi_temp.downloaded = 1
            self.session.commit()
            return True
        except Exception as e:
            self.log(str(e))
            return False


if __name__ == "__main__":
    sql = DatabaseAccessor(config.database_location)
    backend = Backend(sql)
    # podcasts = sql.get_podcasts_with_downloads_available()
    podcasts = sql.session.query(Podcast).filter(
            Podcast.category == 2).all()
    print(len(podcasts))
    # cats = sql.get_all_categories()
    # for cat in cats:
    #     podcasts2 = sql.get_all_podcasts_with_category(cat)
    #     print(len(podcasts2))
