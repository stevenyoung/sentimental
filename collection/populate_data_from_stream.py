#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweet_dbi
import tweet_stream


def main():
  data = tweet_dbi.StreamData(table='stream_sf')
  db_connxn = data.connection()
  stream = tweet_stream.get_stream('sf')

  for status in stream:
    if status.get('lang'):
      try:
        status['text'] = status['text'].replace('\n', ' ')
        data.do_insert(status, db_connxn)
      except ValueError:
        print status['text']
        print status['lang']
        print status['id']
        print status['created_at']
        print status['user']['screen_name']
        raise
        break
      except UnicodeEncodeError:
        print 'oops'
        raise
        break


if __name__ == '__main__':
  main()
