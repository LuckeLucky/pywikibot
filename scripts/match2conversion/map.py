from mwparserfromhell.nodes import Template
from .external_links import MAP_LINKS

PREFIX = 'map'

class Map(object):

	def __init__(self, index: int, summary: Template) -> None:
		self.prefix = PREFIX + str(index)
		self.map = ''
		self.finished = ''
		self.vod = ''
		self.score1 = ''
		self.score2 = ''

		self.index = index

		self.summary = summary

		self.parameters = {}
		self.halfs = {}
		self.links = {}

	def _remove_map_prefix(self, text: str) -> str:
		if text.startswith(self.prefix):
			return text[len(self.prefix):]
		return text

	def _get_finished(self):
		winner = self.parameters.get(self.prefix + 'win')

		if winner in ['1', '2', '0', 'draw']:
			return 'true'

		if winner == 'skip':
			return 'skip'

		return ''

	def _get_halfs(self):
		halfs = {}

		for paramKey, paramValue in self.parameters.items():
			key = self._remove_map_prefix(paramKey)
			if ('t1firstside' in key or 
				't1ct' in key or 
				't1t' in key or
				't2ct' in key or
				't2t' in key):
				halfs[key] = paramValue
		
		return halfs

	def _get_links(self):
		links = {}

		for paramKey, paramValue in self.parameters.items():
			if paramKey.endswith(str(self.index)):
				key = paramKey[:-1]
				if key in MAP_LINKS:
					links[key] = paramValue

		return links

	def process(self):
		for parameter in self.summary.params:
			name = str(parameter.name)
			#catch map1x
			if self.prefix in name:
				self.parameters[name] = str(parameter.value)
			#catch x1
			if name.endswith(str(self.index)):
				self.parameters[name] = str(parameter.value)

		if 'vodgame' + str(self.index) in self.parameters:
			self.vod = self.parameters['vodgame' + str(self.index)]

		self.map = self.parameters[self.prefix] or ''
		self.finished = self._get_finished()
		self.halfs = self._get_halfs()
		self.links = self._get_links()

		if self.prefix + 'score' in self.parameters:
			score = self.parameters[self.prefix + 'score']
			score = score.split('-', 1)
			self.score1 = score[0] or ''
			self.score2 = score[1] or ''

	def __str__(self) -> str:
		out = '{{Map|map=' + self.map
		if self.score1:
			out = out + '|score1=' + self.score1
		if self.score2:
			out = out + '|score1=' + self.score2
		out = out + '|finished=' + self.finished

		if (not self.halfs) and (not self.links):
			return out + '}}'

		if self.halfs:
			halfsOut = '\n\t\t'
			key = ''
			overtimes = 0
			while(True):
				if not (key + 't1firstside' in self.halfs):
					break
				insertedHalfKeys = False
				for halfKey in [key + 't1firstside', key + 't1ct', key + 't1t', key + 't2ct', key + 't2t']:
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
			out = out + '|vod=' + self.vod

		return out + '}}'