#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweet_dbi


def main():
  stream = tweet_stream.Stream().get_stream('all')
  for status in stream:
    if status.get('lang'):
      try:
        print '%s : %s' % (status['user']['screen_name'], status['text'])
      except:
        print status
        raise

if __name__ == '__main__':
  main()
