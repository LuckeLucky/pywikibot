import re
from mwparserfromhell.nodes import Template

from scripts.utils.parser_helper import get_value
from .external_links import STREAMS, MATCH_LINKS
from .map import Map
from .opponent import Opponent

MAX_MAPS = 10

class Match(object):

	def __init__(self, opponent1: Opponent, opponent2: Opponent, winner: int = 0) -> None:
		self.summary = None

		self.opponent1 = opponent1
		self.opponent2 = opponent2

		self.streams = {}
		self.links = {}

		self.maps = []

		self.date = ''
		self.finished = ''
		self.comment = ''
		self.overturned = ''
		self.nostats = ''
		self.nosides = ''

		self.winner = winner
		self.bestof = 0

	def set_summary(self, summary: Template):
		self.summary = summary

	def _handle_streams(self):
		for parameter in self.summary.params:
			key = str(parameter.name)
			if key in STREAMS:
				self.streams[key] = str(parameter.value)

	def _handle_finished(self):
		self.finished = get_value(self.summary, 'finished')
		if not self.finished:
			if int(self.winner) > 0:
				self.finished = 'true'

	def _handle_links(self):
		for parameter in self.summary.params:
			key = str(parameter.name)
			if key in MATCH_LINKS:
				self.links[key] = str(parameter.value)

		if 'hltv' in self.links:
			result = re.sub(r'(\d*)/.*', '\\1', self.links['hltv'], 0, re.MULTILINE)
			self.links['hltv'] = result

	def process(self):
		#finished can be set via winner of the match
		self._handle_finished()

		if self.summary is None:
			return

		self.date = get_value(self.summary, 'date')

		self._handle_streams()
		self._handle_links()

		self.comment = get_value(self.summary, 'comment')
		self.overturned = get_value(self.summary, 'overturned')
		self.nostats = get_value(self.summary, 'nostats')
		self.nosides = get_value(self.summary, 'nosides')

		for mapIndex in range(1, MAX_MAPS):
			mapX = get_value(self.summary, 'map' + str(mapIndex))
			if mapX:
				map = Map(mapIndex, self.summary)
				self.maps.append(map)
				self.bestof = self.bestof + 1


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

		if self.links:
			out = out + '\n\t'
			for linkKey, linkValue in self.links.items():
				out = out + '|' + linkKey + '=' + linkValue

		if self.comment:
			out = out + '\n\t|comment=' + self.comment

		if self.overturned or self.nostats or self.nosides:
			out = out + '\n\t'
			if self.overturned:
				out = out + '|overturned=' + self.overturned
			if self.nostats:
				out = out + '|nostats=' + self.nostats
			if self.nosides:
				out = out + '|nosides=' + self.nosides

		if self.maps:
			for mapIndex, map in enumerate(self.maps):
				map.process(self.bestof)
				out = out + '\n\t'
				out = out + '|map' + str(mapIndex + 1) + '=' + str(map)

		return out + '\n}}'

