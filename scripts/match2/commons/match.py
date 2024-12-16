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
	'lrthread',
	'preview',
	'interview',
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

	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Match\n    ', indent = '    ', end = '}}')

	def __str__(self) -> str:
		out = [
			('opponent1', str(self.opponents[0])),
			('opponent2', str(self.opponents[1])),
			[('date', self.getValue('date')), ('finished', self.getValue('finished'))],
			('winner', self.getValue('winner'), True),
			('vod', self.getValue('vod'), True)
		]

		return self.generateString(out)
