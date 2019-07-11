import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Podcast(Base):
    __tablename__ = 'podcasts'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    podcast_id = Column(Integer, primary_key = True)
    name = Column(String(250))
    url  = Column(String(250))
    audio = Column(String(250))
    video = Column(String(250))

    def __init__(self,name='',url='',audio='',video=''):
        self.name = name
        self.url = url
        self.audio = audio
        self.video = video

class Episode(Base):
    __tablename__ = 'episodes'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    episode_id = Column(Integer, primary_key = True)
    title = Column(String(100))
    published  = Column(DateTime(250))
    summary = Column(String(500))
    length = Column(Integer)
    audio = Column(Integer)
    href = Column(String(250))
    downloaded = Column(Integer)
    podcast_id = Column(Integer, ForeignKey('podcasts.podcast_id'))
    podcast = relationship(Podcast)

    def __init__(self,title='', published='', summary='',length='',audio='',podcast_id='',href=''):
        self.title = title
        self.published = published
        self.summary = summary
        self.length = length
        self.audio = audio
        self.downloaded = 0
        self.podcast_id = podcast_id
        self.href = href

    def __hash__(self):
        return hash((self.title, self.published))

    def __eq__(self,other):
        return self.title,self.published == other.title,other.published
        # return self['title'] == other['title'] and self['published'] == other['published']

    def __ne__(self,other):
        return not self.__eq__(other)
 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_example2.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)