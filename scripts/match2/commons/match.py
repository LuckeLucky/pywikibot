from typing import List

from .template import Template
from .opponent import Opponent

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

class Match:
	def __init__(self, opponents: List[Opponent], template: Template) -> None:
		self.indent = '    '
		self.opponents: List[Opponent] = opponents
		self.template: Template = template
		if not self.template:
			self.template = Template.createFakeTemplate()
		self.maps: List = []

		self.getMaps()

	def getMaps(self):
		pass

	def __str__(self) -> str:
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		indent = self.indent
		out = ("{{Match\n" +
			f"{indent}|opponent1={str(opponent1)}\n" +
			f"{indent}|opponent2={str(opponent2)}\n" +
			f"{indent}|date={self.template.getValue('date')}\n"
			f"{indent}|finished={self.template.getValue('finished')}\n")

		winner = self.template.getValue('winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		out += "}}"
		return out
