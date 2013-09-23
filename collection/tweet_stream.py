#!/usr/bin/env python
# -*- coding: utf-8 -*-

import twitter
from twitter import twitter_globals
twitter_globals.POST_ACTIONS.append('filter')

import app_settings


class Stream(object):
  def __init__(self):
    self.auth_keys = app_settings.oauth_keys()
    self.oauth = twitter.OAuth(self.auth_keys['token'],
                               self.auth_keys['token secret'],
                               self.auth_keys['key'],
                               self.auth_keys['secret'])

  def get_stream(self, stream='all'):
    stream_api = twitter.TwitterStream(auth=self.oauth)
    if stream is 'sf':
      return stream_api.statuses.filter(locations='-122.75,36.8,-121.75,37.8')
    elif stream is 'geo':
      return stream_api.statuses.filter(locations='-180,-90,180,90')
    else:
      return stream_api.statuses.sample()
