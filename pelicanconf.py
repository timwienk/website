#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import date

AUTHOR = 'Tim Wienk'
SITENAME = 'Tim.Wienk.name'
SITEURL = 'https://tim.wienk.name'
RELATIVE_URLS = False

PATH = 'content'
PLUGIN_PATHS = ['plugins']
OUTPUT_PATH = 'output/'
DELETE_OUTPUT_DIRECTORY = True

TIMEZONE = 'Europe/Amsterdam'
DEFAULT_LANG = 'en'
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

PAGE_PATHS = ['en', 'nl']
ARTICLE_PATHS = ['en/articles', 'nl/articles']
STATIC_PATHS = ['']
STATIC_EXCLUDES = ['data']

ARTICLE_URL = '{lang}/articles/{slug}'
ARTICLE_SAVE_AS = '{lang}/articles/{slug}/index.html'
ARTICLE_LANG_URL = ARTICLE_URL
ARTICLE_LANG_SAVE_AS = ARTICLE_SAVE_AS
DRAFT_URL = '{lang}/articles/{slug}/draft.html'
DRAFT_SAVE_AS = '{lang}/articles/{slug}/draft.html'
DRAFT_LANG_URL = DRAFT_URL
DRAFT_LANG_SAVE_AS = DRAFT_SAVE_AS
PAGE_URL = '{lang}/{slug}'
PAGE_SAVE_AS = '{lang}/{slug}/index.html'
PAGE_LANG_URL = PAGE_URL
PAGE_LANG_SAVE_AS = PAGE_SAVE_AS
ARCHIVES_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
INDEX_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
TAG_SAVE_AS = ''
TAGS_SAVE_AS = ''

USE_FOLDER_AS_CATEGORY = False
DISPLAY_CATEGORIES_ON_MENU = False
DEFAULT_PAGINATION = False
DEFAULT_CATEGORY = 'article'

SLUG_SUBSTITUTIONS = (
	('&', 'and'),
)

PATH_METADATA = '(?P<lang>[a-z]{2})/(?:articles/(?P<date>\d{4}\d{2}\d{2})\.)?(?P<slug>.*)\.[a-z]{1,4}'
EXTRA_PATH_METADATA = {
	'en/index.md': {'save_as': 'en/index.html', 'url': 'en'},
	'nl/index.md': {'save_as': 'nl/index.html', 'url': 'nl'},
	'en/error/400.md': {'save_as': 'error/400.html', 'status': 'hidden'},
	'en/error/401.md': {'save_as': 'error/401.html', 'status': 'hidden'},
	'en/error/403.md': {'save_as': 'error/403.html', 'status': 'hidden'},
	'en/error/404.md': {'save_as': 'error/404.html', 'status': 'hidden'},
	'en/error/410.md': {'save_as': 'error/410.html', 'status': 'hidden'},
	'en/error/500.md': {'save_as': 'error/500.html', 'status': 'hidden'},
}

PLUGINS = ['neighbors', 'githubcontributions', 'touch', 'sitemap']
THEME = 'theme'
THEME_STATIC_DIR = ''

MARKDOWN = {
	'extensions': ['extra', 'headerid', 'meta', 'plugins.markdown_customsection'],
	'extension_configs': {
		'codehilite': {
			'linenums': False,
			'guess_lang': False,
			'css_class': 'code',
		},
	},
	'output_format': 'xhtml5',
}
JINJA_ENVIRONMENT = {
	'extensions': ['jinja2.ext.i18n'],
}

FEED_ALL_ATOM = 'atom.xml'
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = '%s/atom.xml'

SITEMAP = {
	'format': 'xml',
	'extra_files': ['media/cv/timwienk-cv-nederlands.pdf', 'media/cv/timwienk-cv-english.pdf']
}

SOCIAL = (
    ('GitHub', 'https://github.com/timwienk', '/timwienk'),
    ('LinkedIn', 'https://www.linkedin.com/in/timwienk', '/in/timwienk'),
    ('Twitter', 'https://twitter.com/timwienk', '@timwienk'),
    ('Facebook', 'https://www.facebook.com/timwienk', '/timwienk'),
    ('Google+', 'https://plus.google.com/+TimWienk', '+timwienk'),
)
GITHUB_USER = 'timwienk'
FACEBOOK_USER = 'timwienk'
TWITTER_USER = 'timwienk'

FIRST_YEAR = 1989
LAST_YEAR = date.today().year

GOOGLE_ANALYTICS = 'UA-7267499-1'
GOOGLE_ANALYTICS_ID_SCRIPT = '/scripts/id'
