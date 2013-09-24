#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweet_dbi
import tweet_stream


def main():
  streamdata = tweet_dbi.StreamData(table='stream_sf_dev')
  db_connxn = streamdata.connection()
  stream = tweet_stream.Stream().get_stream('sf')
  hashtags = tweet_dbi.Hashtags(table='stream_sf_hashtags')

  for status in stream:
    if status.get('lang'):
      try:
        status['text'] = status['text'].replace('\n', ' ')
        streamdata.do_insert(status, db_connxn)
        print '%s : %s' % (status['user']['screen_name'], status['text'])
        for tag in status['entities']['hashtags']:
          hashtags.do_insert(tag, status['id'], db_connxn)
          print '%s : %s' % (tag['text'], tag['indices'][0])
      except ValueError:
        print status['text']
        print status['lang']
        print status['id']
        print status['created_at']
        print status['user']['screen_name']
        raise
      except UnicodeEncodeError:
        print 'oops'
        raise


if __name__ == '__main__':
  main()
