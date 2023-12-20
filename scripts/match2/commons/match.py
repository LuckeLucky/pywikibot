from typing import List
from mwparserfromhell.nodes import Template

from .opponent import Opponent
from .utils import sanitizeTemplate, getTemplateParameters

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
	def __init__(self, opponents: List[Opponent], template: Template, isReset: bool = False) -> None:
		self.opponents = opponents
		self.template = sanitizeTemplate(template)
		self.isReset = isReset
		self.data = getTemplateParameters(self.template)
		self.maps = []

		self.getMaps()

	def isValidResetOrThird(self) -> bool:
		for opponent in self.opponents:
			if opponent.score:
				return True

		for key, val in self.data.items():
			if val:
				#We dont check winner because for reset match final winner == reset winner (match1)
				if key != 'winner':
					return True
				if key == 'winner' and not self.isReset:
					return True
		return False

	def getMaps(self):
		pass
