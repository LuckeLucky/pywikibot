from typing import List

from .template import Template
from .opponent import Opponent
from .templateutils import TemplateUtils

STREAMS = [
	'stream',
	'afreeca',
	'afreecatv',
	'bilibili',
	'cc163',
	'dailymotion',
	'douyu',
	'facebook',
	'huomao',
	'huya',
	'loco',
	'mildom',
	'nimo',
	'tl',
	'trovo',
	'twitch',
	'twitch2',
	'youtube',
]

class Match(TemplateUtils):
	def __init__(self, opponents: List[Opponent], template: Template) -> None:
		self.indent = '    '
		self.opponents: List[Opponent] = opponents
		super().__init__(template)
		self.maps: List = []

		self.getMaps()

	def getMaps(self):
		pass

	def print(self, params: List[str]) -> str:
		return super().printTemplate(params, templateId = 'Match', indent = '    ', end = '}}', ignoreEmptyParams = True)

	def __str__(self) -> str:
		out = [
			f'|opponent1={str(self.opponents[0])}' + '\n',
			f'|opponent2={str(self.opponents[1])}' + '\n',
			self.printParam('date', end = self.printParam('finished', end = '\n')),
			self.printParam('winner', ignoreIfEmpty=True, end = '\n'),
			self.printParam('vod', end='\n', ignoreIfEmpty=True)
		]

		return self.print(out)
