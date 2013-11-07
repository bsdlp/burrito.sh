#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'jchen'
SITENAME = u'BURRITO 4 LYFE'
SITEURL = ''

TIMEZONE = 'ETC/UTC'

DEFAULT_LANG = u'en'

CSS_FILE = 'style.css'

# theme stuff
THEME = '/Users/jchen/git/pelican/burrito'

# plugins
PLUGIN_PATH = '/Users/jchen/git/pelican/plugins-pelican'
PLUGINS = ['gravatar']

# gravatar email
AUTHOR_EMAIL = 'fly@sjchen.net'

# social
TWITTER_USERNAME = 's_jchen'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

# PLUGINS = ['pelican_youtube',]


DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
