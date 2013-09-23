#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Organize data from MySQL or CSV source into training, testing sets for models.
# Currently connecting but collection and exploration should be using same
# interface for db.

# Updating this would also allow simple interface for queries used for other
# uses, validation, etc.

import csv
import numpy as np

import MySQLdb

# column index:
# 0 id
# 1 ts
# 2 text
# 3 lang
# 4 status_id
# 5 created
# 6 screenname
# 7 favorited
# 8 retweeted
# 9 reply_to
# 10 favorite_count
# 11 user_id
# 12 user_followers
# 13 user_listed_count
# 14 user_statuses_count
# 15 user_favorites_count
# 16 retweet_count
# 17 user_friends_count
# 18 sentiment
# 19 geo
# 20 box_sw
# 21 box_nw
# 22 box_ne
# 23 box_se
# 24 lat
# 25 lng
# 26 positive_word_count
# 27 negative_word_count
# 28 word_count
# 29 meaning_word_count

# column indices of input variables
WORD_COUNT = 28
IMPORTANT_WORD_COUNT = 29
LAT = 24
LNG = 25
FOLLOWERS = 12
LISTED_COUNT = 13
STATUS_COUNT = 14
FAVORITES_COUNT = 15
FRIENDS = 17

# output variables
POSITIVE_WORD_COUNT = 26
NEGATIVE_WORD_COUNT = 27


def get_db_cursor():
  con = MySQLdb.connect('mysql.eyeballschool.tv', 'tweetstream', 'arafat',
                        'ebs_tweets')
  return con.cursor()


def training_data_from_db():
  # Pull training samples from db
  # pull all variables for all observations
  X = []
  y = []
  cur = get_db_cursor()
  query = 'select * from `stream_sf`'
  cur.execute(query)
  inputs = [WORD_COUNT, IMPORTANT_WORD_COUNT, LAT, LNG, FOLLOWERS, LISTED_COUNT,
            STATUS_COUNT, FAVORITES_COUNT, FRIENDS]
  outputs = POSITIVE_WORD_COUNT

  # contains more positive words than negative words?
  # assign NEGATIVE_WORD_COUNT to outputs above to check for likelihood of more
  # negative words than positive

  for row in cur.fetchall():
    tmp = []
    if row[outputs] > 0:
      y.append(1)
    else:
      y.append(0)
    for i in inputs:
      tmp.append(row[i])
    X.append(tmp)
  return np.array(X), np.array(y)


def organize_data(data):
  X = []
  y = []
  # inputs = [28, 29, 24, 25, 12, 13, 14, 15, 17]
  # outputs = 26
  inputs = [WORD_COUNT, IMPORTANT_WORD_COUNT, LAT, LNG, FOLLOWERS, LISTED_COUNT,
            STATUS_COUNT, FAVORITES_COUNT, FRIENDS]
  outputs = POSITIVE_WORD_COUNT
  for d in data:
    try:
      print len(d)
      tmp = []
      for i in inputs:
        tmp.append(d[i])

      X.append(tmp)

      # contains more positive words than negative words
      # update outputs
      # to check for likelihood of more negative words than positive

      if int(d[outputs]) > 0:
          y.append(1)
      else:
          y.append(0)
      # print X, y
    except:
      print d, len(d)
      print d[0], d[2], d[3], d[4], d[24]

      pass

  return np.array(X), np.array(y)


def load_data_from_csv():
  # get training data from a csv dump
  #data = csv.reader(open('query_result.csv', 'rb'))
  data = csv.reader(open('stream_sf.csv', 'rb'))
  return organize_data(data)


def load_test_data():
  # get test data from a csv dump
  data = csv.reader(open('stream_sf_view.csv', 'rb'))
  return organize_data(data)
