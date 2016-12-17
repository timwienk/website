from __future__ import unicode_literals
import json
import logging
import os
from time import sleep

try:
	from urllib2 import urlopen
	from urllib2 import HTTPError
except ImportError:
	from urllib.request import urlopen
	from urllib.request import HTTPError

from pelican import signals

logger = logging.getLogger(__name__)
GITHUB_API = 'https://api.github.com/repos/{0}/stats/contributors'


class Project(object):

	def __init__(self, plugin, data, cache):
		self.plugin = plugin

		if hasattr(data, 'iteritems'):
			iterator = data.iteritems()
		else:
			iterator = data.items()

		for k, v in iterator:
			if k not in ['additions', 'deletions', 'commits']:
				setattr(self, k, v)

		if cache is None:
			logger.info('Fetching data for github project: %s', data['repository'])
			self.stats = self.get_stats(data)
			plugin.save_cache(data['repository'], self.stats)
		else:
			logger.info('Using cache for github project: %s', data['repository'])
			self.stats = cache

	def get_stats(self, defaults):
		url = GITHUB_API.format(self.repository)

		stats = {
			'additions': defaults['additions'] if 'additions' in defaults else 0,
			'deletions': defaults['deletions'] if 'deletions' in defaults else 0,
			'commits': defaults['commits'] if 'commits' in defaults else 0,
		}

		for data in self.load(url):
			if data['author']['login'] == self.plugin.gen.settings['GITHUB_USER']:
				for week in data['weeks']:
					stats['additions'] += week['a']
					stats['deletions'] += week['d']
					stats['commits'] += week['c']

		return stats

	def load(self, url):
		try:
			response = urlopen(url)
		except HTTPError:
			logger.warning('Error opening {0}'.format(url))
			return

		if response.getcode() == 202:
			sleep(2)
			return self.load(url)

		# 3 vs 2 makes us have to do nasty stuff to get encoding without
		# being 3 or 2 specific. So... Yeah.
		encoding = response.headers['content-type'].split('charset=')[-1]
		data = response.read().decode(encoding)

		return json.loads(data)


class GithubContributions(object):

	def __init__(self, gen):
		self.gen = gen
		self.projects = []

		if not 'GITHUB_USER' in gen.settings.keys():
			logger.warning('GITHUB_USER is not set for GithubContributions plugin')
		else:
			projects = self.load_projects()
			cache = self.load_cache()
			for project in projects:
				if 'repository' in project:
					project_cache = None
					if project['repository'] in cache:
						project_cache = cache[project['repository']]
					self.projects.append(Project(self, project, project_cache))

	def load_projects(self):
		projects = []

		path = os.path.join(self.gen.settings['PATH'], 'data/projects.json')
		if os.path.isfile(path):
			with open(path) as file:
				projects = json.load(file)

		return projects

	def load_cache(self):
		self.cache = {}

		path = os.path.join(self.gen.settings['PATH'], 'data/projects_cache.json')
		if os.path.isfile(path):
			with open(path) as file:
				self.cache = json.load(file)

		return self.cache

	def save_cache(self, repository, data):
		self.cache[repository] = data
		self.write_cache()

	def write_cache(self):
		path = os.path.join(self.gen.settings['PATH'], 'data/projects_cache.json')
		try:
			file = open(path, 'w')
		except IOError:
			logger.warning('Cannot write {0}'.format(path))
		else:
			with file:
				json.dump(self.cache, file, indent=2)

	def fetch(self):
		return self.projects


def initialize(gen):
	gen.plugin_instance = GithubContributions(gen)


def fetch(gen, metadata):
	gen.context['github_project_contributions'] = gen.plugin_instance.fetch()


def register():
	signals.page_generator_init.connect(initialize)
	signals.page_generator_context.connect(fetch)
