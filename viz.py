#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas.io.sql as psql
import MySQLdb

from pandas import read_csv
import csv

def load_table_into_df(table='stream_sf'):
  con = MySQLdb.connect(host='localhost', user='root', db='ebs_tweets')
  query = 'SELECT * from %s' % (table)
  return psql.read_frame(query, con)


def write_df_to_csv(df, filename='stream_sf'):
  return df.to_csv('html/csv/' + filename + '.csv')


def data_for_time_series_charts():
  def flatten_creation_date(row):
    row['created']

  tweets = load_table_into_df()
  tweets['date'
  ts_data = tweets[['created', 'sentiment']]
  tweets.apply(flatten_creation_date, axis=1)

  # we want frequency of tweets per hour
  write_df_to_csv(ts_data)

  # load located
  # not that we have locations we want
  # to create a json
  locations = 