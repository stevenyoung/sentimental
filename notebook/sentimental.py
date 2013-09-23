# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import extraction

# <codecell>

extraction.main()

# <codecell>

import MySQLdb
import pandas.io.sql as sql
import pandas as pd

# <markdowncell>

# Pull tweet data from local DB table.

# <codecell>

con = MySQLdb.connect('localhost', 'root', '', 'ebs_tweets')
query = 'SELECT * from sf_stream'
data_frame = sql.read_frame(query, con)

# <codecell>

data_frame

# <codecell>

import sqlalchemy
from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker

# <codecell>

class Tweets(object):
    pass

def loadSession():
  db_engine = create_engine('mysql://root@localhost/ebs_tweets')
  metadata = MetaData(db_engine)
  tweets_table = Table('sf_statuses', metadata, autoload=True)
  mapper(Tweets, tweets_table)
  Session = sessionmaker(bind=db_engine)
  session = Session()
  return session

@contextmanager
def session_scope():
  session = loadSession()
  try:
    yield session
    session.commit()
  except:
    session.rollback()
    raise
  finally:
    session.close()

# <codecell>

with session_scope() as session:
    res = session.query(Tweets).all()
    for r in res:
        print r.text, r.ts, r.location

# <codecell>

messages = []
res = session.query(Tweets).all()
for r in res:
    messages.append(r.text)
print messages
        

# <codecell>

with session_scope() as session:
    res = session.query(Tweets).all()
    res = session.query(Tweets).select(
    for r in res:
      print r.text, r.ts, r.location
      if str(r.geo).startswith('[['):
        points = (r.geo).split(', [')
        (lats, lngs) = ([], [])
        for point in points:
          l = point.split(',')
          lng = l[0].replace('[', '')
          lat = l[1].replace(']', '')
          lats.append(lat)
          lngs.append(lng)
        print lats, lngs
        box_1_lat = min(lats)
        box_1_lng = min(lngs)
        box_2_lat = max(lats)
        box_2_lng = min(lngs)
        box_3_lat = min(lats)
        box_3_lng = max(lngs)
        box_4_lat = max(lats)
        box_4_lng = max(lngs)
        print box_1_lat, box_1_lng, box_2_lat, box_2_lng, box_3_lat, box_3_lng, box_4_lat, box_4_lng
        
        break
      else:
        l = (r.geo).split(',')
        lat = l[0].replace('[', '')
        lng = l[1].replace(']', '')
        print lat, lng
        geom_text = '({}, {})'.format(lat, lng)
        upd_stmt = 

# <codecell>

len(messages)

# <codecell>


# <codecell>


# <codecell>


