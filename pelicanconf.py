#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'jchen'
AUTHOR_FULLNAME = u'Jon Chen'
SITENAME = u'burritos r us'
SITEURL = 'http://burrito.sh'

TIMEZONE = 'ETC/UTC'

DEFAULT_LANG = u'en'

CSS_FILE = 'style.css'

# theme stuff
THEME = './theme'

# plugins
PLUGIN_PATH = './plugins'
PLUGINS = ['gravatar', 'thumbnailer']

# gravatar email
AUTHOR_EMAIL = 'dabestmayne@burrito.sh'

# social
TWITTER_USERNAME = 's_jchen'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = 10

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_MENUITEMS_ON_MENU = False
DISPLAY_NAVBAR = False
DISPLAY_PAGES_ON_MENU = False

DEFAULT_DATE_FORMAT = ('%Y-%m-%d')

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# add paths to pelican
STATIC_PATHS = ['img']

# Thumbnailer plugin options
IMAGE_PATH = 'img'
THUMBNAIL_DIR = 'thumbs'
THUMBNAIL_SIZES = {
    'thumbnail_square': '270',
    'thumbnail_wide': '540x?',
}

PYGMENTS_RST_OPTIONS = {
    'linenos': 'table',
}

MD_EXTENSIONS = ['codehilite(css_class=highlight, linenums=True)','extra']

