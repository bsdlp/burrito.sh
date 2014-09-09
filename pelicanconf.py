#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'jchen'
AUTHOR_FULLNAME = u'Jon Chen'
SITENAME = u'burrito'
SITEURL = 'http://burrito.sh'
SITETAGLINE = 'Excelling at mediocrity.'

TIMEZONE = 'Etc/UTC'

DEFAULT_LANG = u'en'

# theme stuff
THEME = './theme'

# plugins
PLUGIN_PATHS = ['./plugins', './plugins.d']
PLUGINS = ['assets', 'summary', 'thumbnailer', 'pelican-dynamic']

# gravatar email
AUTHOR_EMAIL = 'dabestmayne@burrito.sh'

# social
TWITTER_USERNAME = 's_jchen'

GOOGLE_ANALYTICS = 'UA-47876445-1'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = 4

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_MENUITEMS_ON_MENU = False
DISPLAY_NAVBAR = False
DISPLAY_PAGES_ON_MENU = True

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

OUTPUT_RETENTION = ("keybase.txt")

DEFAULT_DATE_FORMAT = ('%Y-%m-%d')

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# add paths to pelican
STATIC_PATHS = ['img']

# Thumbnailer plugin options
IMAGE_PATH = 'img'
THUMBNAIL_DIR = 'thumbs'
THUMBNAIL_SIZES = {
    'thumbnail_square': '317',
    'thumbnail_wide': '635x?',
}

# markdown extensions for syntax highlighting
MD_EXTENSIONS = ['codehilite(css_class=highlight, linenums=False)','extra']

WEBASSETS = True

ARTICLE_URL = 'posts/{date:%Y}{date:%m}{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}{date:%m}{date:%d}/{slug}/index.html'
