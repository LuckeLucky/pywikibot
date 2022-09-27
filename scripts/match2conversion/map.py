from mwparserfromhell.nodes import Template
from .external_links import MAP_LINKS
from scripts.utils.parser_helper import get_value, dict_has_value_set

PREFIX = 'map'

class Map(object):

	def __init__(self, index: int, summary: Template) -> None:
		self.prefix = PREFIX + str(index)
		self.map = ''
		self.finished = ''
		self.vod = ''
		self.vod2 = ''
		self.score = ''
		self.score1 = ''
		self.score2 = ''
		self.winner = -1

		self.index = index

		self.summary = summary

		self.halfs = {}
		self.links = {}

	def _remove_map_prefix(self, text: str) -> str:
		if text.startswith(self.prefix):
			return text[len(self.prefix):]
		return text

	def populate_winner_and_finished(self):
		winner = get_value(self.summary, self.prefix + 'win')
		if winner in ['1', '2', '0']:
			self.winner = int(winner)
			self.finished = 'true'
		elif winner == 'draw':
			self.winner = 0
			self.finished = 'true'
		elif winner == 'skip':
			self.finished = 'skip'

	def populate_halfs(self):
		for parameter in self.summary.params:
			key = str(parameter.name)
			#Ignore other maps
			if not(self.prefix in key):
				continue
			if ('t1firstside' in key or 
				't1ct' in key or 
				't1t' in key or
				't2ct' in key or
				't2t' in key):
				self.halfs[self._remove_map_prefix(key)] = str(parameter.value)

	def populate_links(self, bestof):
		for parameter in self.summary.params:
			key = str(parameter.name)
			#catch parameters like eseaX
			if key.endswith(str(self.index)):
				key = key[:-1]
				if key in MAP_LINKS:
					self.links[key] = str(parameter.value)
			#In bestof 1 sometimes parameters like esea exist intead of eseaX
			if bestof == 1:
				if key in MAP_LINKS:
					self.links[key] = str(parameter.value)

	def process(self, bestof):
		if self.summary is None:
			return

		self.map = get_value(self.summary, self.prefix)

		self.score = get_value(self.summary, self.prefix + 'score')
		if self.score:
			self.score1, self.score2 = self.score.split('-', 1)

		self.vod = get_value(self.summary, 'vodgame' + str(self.index))
		self.vod2 = get_value(self.summary, '2vodgame' + str(self.index))

		self.populate_winner_and_finished()
		self.populate_halfs()
		self.populate_links(bestof)

	def __str__(self) -> str:
		out = '{{Map|map=' + self.map
		if self.score1:
			out = out + '|score1=' + self.score1
		if self.score2:
			out = out + '|score2=' + self.score2
		out = out + '|finished=' + self.finished

		if self.finished == 'skip':
			return out + '}}'

		#Sometimes only the winner is set
		if (not self.score) and (not dict_has_value_set(self.halfs)) and (self.winner > -1) and (not self.vod):
			out = out + '|winner=' + str(self.winner)
			return out + '}}'

		if self.halfs:
			halfsOut = '\n\t\t'
			key = ''
			overtimes = 0
			while(True):
				if not (key + 't1firstside' in self.halfs):
					break
				insertedHalfKeys = False
				for halfKey in [key + 't1firstside', key + 't1t', key + 't1ct', key + 't2t', key + 't2ct']:
					if halfKey in self.halfs:
						halfsOut = halfsOut + '|' + halfKey + '=' + self.halfs[halfKey]
						insertedHalfKeys = True
				if insertedHalfKeys and ((overtimes + 1) * 5) < len(self.halfs):
					halfsOut = halfsOut + '\n\t\t'
				overtimes += 1
				key = 'o' + str(overtimes)
	
			out = out + halfsOut

		if self.links:
			linksOut = '\n\t\t'
			for linkKey, linkValue in self.links.items():
				linksOut = linksOut + '|' + linkKey + '=' + linkValue
			out = out + linksOut

		if self.vod:
			if not self.links:
				out = out + '\n\t\t'
			out = out + '|vod=' + self.vod

		if self.vod and self.vod2:
			out = out + '|vod2=' + self.vod2

		return out + '}}'