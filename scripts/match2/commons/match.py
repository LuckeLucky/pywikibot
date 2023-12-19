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

class Match(object):
	def __init__(self, opponents: List[Opponent], template: Template) -> None:
		self.opponents = opponents
		self.template = sanitizeTemplate(template)
		self.data = getTemplateParameters(self.template)
		self.maps = []

		self.getMaps()

	def isValid(self) -> bool:
		return (self.opponents[0] and self.opponents[1]) or self.template

	def getMaps(self):
		pass
