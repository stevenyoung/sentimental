#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
from twitter import twitter_globals
twitter_globals.POST_ACTIONS.append('filter')

import app_settings

def get_stream(stream='all'):
  oa = app_settings.oauth_keys()
  auth = twitter.OAuth(oa['token'], oa['token secret'], oa['key'], oa['secret'])
  stream_api = twitter.TwitterStream(auth=auth)
  
  if stream is 'sf':
    return stream_api.statuses.filter(locations='-122.75,36.8,-121.75,37.8')
  elif stream is 'geo':
    return stream_api.statuses.filter(locations='-180,-90,180,90')
  else:
    return stream_api.statuses.sample()

