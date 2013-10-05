#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import time

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

import app_settings
import sentiment


class BaseModel(object):
  def __init__(self):
    self.db_engine = create_engine(app_settings.db_engine())
    self.metadata = MetaData(self.db_engine)

  def connection(self):
    return self.db_engine.connect()


class Users(BaseModel):
  def __init__(self, table='stream_sf_users'):
    super(Users, self).__init__()
    self.users = Table(table, self.metadata, autoload=True)


class Hashtags(BaseModel):
  def __init__(self, table='stream_sf_hashtags'):
    super(Hashtags, self).__init__()
    self.hashtags = Table(table, self.metadata, autoload=True)

  def do_insert(self, hashtag, status_id, db_connxn):
    db_connxn.execute(self.hashtags.insert(),
                      status_id=status_id,
                      hashtag=hashtag['text'],
                      start=hashtag['indices'][0],
                      end=hashtag['indices'][1]
                      )


class StreamData(BaseModel):
  def __init__(self, table='stream_sf'):
    super(StreamData, self).__init__()
    self.tweets = Table(table, self.metadata, autoload=True)

  def format_geo_coords(self, geo):
    if str(geo).startswith('[['):
      lat = float(geo[0][0][1] + geo[0][2][1])/2
      lng = float(geo[0][0][0] + geo[0][2][0])/2
      box_sw = '({0}, {1})'.format(geo[0][0][1], geo[0][0][0])
      box_se = '({0}, {1})'.format(geo[0][1][1], geo[0][1][0])
      box_ne = '({0}, {1})'.format(geo[0][2][1], geo[0][2][0])
      box_nw = '({0}, {1})'.format(geo[0][3][1], geo[0][3][0])
    else:
      lat = geo[0]
      lng = geo[1]
      box_sw = None
      box_se = None
      box_ne = None
      box_nw = None
    geo_coords = '({0}, {1})'.format(lat, lng)
    return {'lat': lat, 'lng': lng, 'geom': geo_coords, 'box_sw': box_sw,
            'box_se': box_se, 'box_ne': box_ne, 'box_nw': box_nw}

  def do_insert(self, status_msg, db_connxn):
    table = string.maketrans("", "")

    # Clean up the text
    text = string.translate(status_msg['text'].encode('ascii', 'ignore'), table)
    text = text.replace('\'', '')

    lang = status_msg['lang']
    status_id = status_msg['id']
    created = time.strptime(status_msg['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    created = time.strftime('%Y-%m-%d %H:%M:%S', created)
    reply_to = 0
    if status_msg['in_reply_to_status_id']:
      reply_to = status_msg['in_reply_to_status_id']

    geo = status_msg['geo']
    if geo:
      geo = status_msg['geo']['coordinates']
    elif status_msg.get('place'):
      geo = status_msg['place']['bounding_box']['coordinates']

    loc = self.format_geo_coords(geo)
    score = sentiment.score_sentiment(text)
    tweet_sentiment = score['positive matches'] - score['negative matches']
    hashtag_count = len(status_msg['entities']['hashtags'])

    db_connxn.execute(self.tweets.insert(), text=text, lang=lang, status_id=status_id,
                      created=created, reply_to=reply_to,
                      screenname=status_msg['user']['screen_name'],
                      sentiment=tweet_sentiment,
                      user_id=status_msg['user']['id'],
                      user_followers=status_msg['user']['followers_count'],
                      user_listed_count=status_msg['user']['listed_count'],
                      user_statuses_count=status_msg['user']['statuses_count'],
                      user_friends_count=status_msg['user']['friends_count'],
                      user_favorites_count=status_msg['user']['favourites_count'],
                      favorite_count=status_msg['favorite_count'],
                      retweet_count=status_msg['retweet_count'],
                      favorited=status_msg['favorited'],
                      retweeted=status_msg['retweeted'],
                      positive_word_count=score['positive matches'],
                      negative_word_count=score['negative matches'],
                      word_count=score['word count'],
                      meaning_word_count=score['meaning word count'],
                      geo=loc['geom'],
                      box_sw=loc['box_sw'],
                      box_se=loc['box_se'],
                      box_ne=loc['box_ne'],
                      box_nw=loc['box_nw'],
                      lat=loc['lat'],
                      lng=loc['lng'],
                      hashtag_count=hashtag_count)


class Tweet(object):
  pass


class TweetData(object):
  def __init__(self, table='stream_sf'):
    self.db_engine = create_engine(app_settings.db_engine())
    metadata = MetaData(self.db_engine)
    super(TweetData, self).__init__()
    self.tweets = Table(table, metadata, autoload=True)

  def loadSession(self):
    # db_engine = create_engine('mysql://root@localhost/ebs_tweets')
    # print 'create engine'
    # metadata = MetaData(db_engine)
    # print 'metadata', metadata
    # tweets_table = Table('sf_stream_again', metadata, autoload=True)
    # print 'table', tweets_table
    # mapper(Tweet, tweets_table)
    mapper(Tweet, self.tweets)
    # print 'mapper'
    Session = sessionmaker(bind=self.db_engine)
    session = Session()
    return session

  @contextmanager
  def session_scope(self):
    session = self.loadSession()
    try:
      yield session
      session.commit()
    except:
      session.rollback()
      raise
    finally:
      session.close()
