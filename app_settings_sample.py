#!/usr/bin/env python
# -*- coding: utf-8 -*-


def oauth_keys():
  CONSUMER_KEY = ''
  CONSUMER_SECRET = ''
  OAUTH_TOKEN = ''
  OAUTH_TOKEN_SECRET = ''
  return {'key': CONSUMER_KEY, 'secret': CONSUMER_SECRET, 'token': OAUTH_TOKEN,
          'token secret': OAUTH_TOKEN_SECRET}


def db_engine():
  return 'mysql://user:pass@host/db'
