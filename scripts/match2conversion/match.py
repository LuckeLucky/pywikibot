import re
from os import link
from mwparserfromhell.nodes import Template
from .external_links import ALL_LINKS, STREAMS, MAP_LINKS, MATCH_LINKS
from .map import Map
from .opponent import Opponent

MAX_MAPS = 10

class Match(object):

	def __init__(self, opponent1: Opponent, opponent2: Opponent) -> None:
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

	def set_summary(self, summary: Template):
		self.summary = summary

	def _get_streams(self):
		streams = {}

		for paramKey, paramValue in self.parameters.items():
			if paramKey in STREAMS:
				streams[paramKey] = paramValue

		return streams

	def _get_links(self):
		links = {}

		for paramKey, paramValue in self.parameters.items():
			if paramKey in ALL_LINKS:
				links[paramKey] = paramValue

		if 'hltv' in links:
			result = re.sub(r'(\d*)/.*', '\\1', links['hltv'], 0, re.MULTILINE)
			links['hltv'] = result

		return links

	def process(self):
		if self.summary is None:
			return

		for parameter in self.summary.params:
			self.parameters[str(parameter.name)] = str(parameter.value)

		if 'date' in self.parameters:
			self.date = self.parameters['date']

		if 'finished' in self.parameters:
			self.finished = self.parameters['finished']

		if 'vod' in self.parameters:
			self.vod = self.parameters['vod']

		if 'comment' in self.parameters:
			self.comment = self.parameters['comment']

		if 'overturned' in self.parameters:
			self.overturned = self.parameters['overturned']

		self.streams = self._get_streams()
		self.links = self._get_links()

		for mapIndex in range(1, MAX_MAPS):
			if 'map' + str(mapIndex) in self.parameters:
				map = Map(mapIndex, self.summary)
				map.process()
				self.maps.append(map)

	def __str__(self) -> str:
		out = '{{Match'

		if self.opponent1:
			out = out + '\n\t|opponent1=' + str(self.opponent1)
		if self.opponent2:
			out = out + '|opponent2=' + str(self.opponent2)

		out = out + '\n\t|date=' + self.date + '|finished=' + self.finished
		if self.streams:
			out = out + '\n\t'
			for streamKey, streamValue in self.streams.items():
				out = out + '|' + streamKey + '=' + streamValue

		if self.vod:
			out = out + '|vod=' + self.vod

		if self.links:
			out = out + '\n\t'
			for linkKey, linkValue in self.links.items():
				out = out + '|' + linkKey + '=' + linkValue

		if self.comment:
			out = out + '\n\t|comment=' + self.comment

		if self.overturned:
			out = out + '\n\t|overturned=' + self.overturned

		if self.maps:
			for mapIndex, map in enumerate(self.maps):
				out = out + '\n\t'
				out = out + '|map' + str(mapIndex + 1) + '=' + str(map)

		return out + '\n}}'

