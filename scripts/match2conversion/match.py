import re
from os import link
from mwparserfromhell.nodes import Template
from .external_links import STREAMS, MATCH_LINKS
from .map import Map
from .opponent import Opponent

MAX_MAPS = 10

class Match(object):

	def __init__(self, opponent1: Opponent, opponent2: Opponent, winner: int = 0) -> None:
		self.summary = None

		self.opponent1 = opponent1
		self.opponent2 = opponent2

		self.parameters = {}
		self.streams = {}
		self.links = {}

		self.maps = []

		self.date = ''
		self.finished = ''
		self.vod = ''
		self.comment = ''
		self.overturned = ''

		self.winner = winner
		self.bestof = 0

	def set_summary(self, summary: Template):
		self.summary = summary

	def _get_streams(self):
		streams = {}

		for paramKey, paramValue in self.parameters.items():
			if paramKey in STREAMS:
				streams[paramKey] = paramValue

		return streams

	def handle_finished(self):
		self.finished = self.parameters['finished']

		if not self.finished:
			if self.winner > 0:
				self.finished = 'true'

	def handle_links(self):
		for paramKey, paramValue in self.parameters.items():
			if paramKey in MATCH_LINKS:
				self.links[paramKey] = paramValue

		if 'hltv' in self.links:
			result = re.sub(r'(\d*)/.*', '\\1', self.links['hltv'], 0, re.MULTILINE)
			self.links['hltv'] = result

	def process(self):
		if self.summary is None:
			return

		for parameter in self.summary.params:
			self.parameters[str(parameter.name)] = str(parameter.value)

		if 'date' in self.parameters:
			self.date = self.parameters['date']
			
		self.handle_finished()

		if 'vod' in self.parameters:
			self.vod = self.parameters['vod']

		if 'comment' in self.parameters:
			self.comment = self.parameters['comment']

		if 'overturned' in self.parameters:
			self.overturned = self.parameters['overturned']

		#Stats for bo1
		if 'stats' in self.parameters:
			self.summary.remove('stats')
			self.summary.add('stats1', self.parameters.pop('stats'))


		self.streams = self._get_streams()

		for mapIndex in range(1, MAX_MAPS):
			if 'map' + str(mapIndex) in self.parameters:
				map = Map(mapIndex, self.summary)
				self.maps.append(map)
				self.bestof = self.bestof + 1

		self.handle_links()

	def __str__(self) -> str:
		out = '{{Match'

		if self.opponent1:
			out = out + '\n\t|opponent1=' + str(self.opponent1)
		if self.opponent2:
			out = out + '|opponent2=' + str(self.opponent2)

		if self.finished and (not self.date):
			out = out + '\n\t|finished=' + self.finished
		else:
			out = out + '\n\t|date=' + self.date + '|finished=' + self.finished

		if self.streams:
			out = out + '\n\t'
			for streamKey, streamValue in self.streams.items():
				out = out + '|' + streamKey + '=' + streamValue

		if self.vod:
			if not self.streams:
				out = out + '\n\t'
			out = out + '|vod=' + self.vod

		if self.links:
			out = out + '\n\t'
			self.handle_links()
			for linkKey, linkValue in self.links.items():
				out = out + '|' + linkKey + '=' + linkValue

		if self.comment:
			out = out + '\n\t|comment=' + self.comment

		if self.overturned:
			out = out + '\n\t|overturned=' + self.overturned

		if self.maps:
			for mapIndex, map in enumerate(self.maps):
				map.process()
				map.handle_links(self.bestof)
				out = out + '\n\t'
				out = out + '|map' + str(mapIndex + 1) + '=' + str(map)

		return out + '\n}}'

