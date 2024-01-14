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
		self.indent = '  '
		self.opponents: List[Opponent] = opponents
		self.template: Template = template
		if not self.template:
			self.template = Template.createFakeTemplate()
		self.maps: List = []

		self.getMaps()

	def getMaps(self):
		pass
