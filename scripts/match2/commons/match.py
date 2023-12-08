from mwparserfromhell.nodes import Template

from .opponent import Opponent
from .utils import *

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
	def __init__(self, opponent1: Opponent, opponent2: Opponent, template: Template) -> None:
		self.opponent1 = opponent1
		self.opponent2 = opponent2
		self.template = sanitize_template(template)
		self.data = template_parameters_to_str_dict(self.template)
		self.maps = []

		self.get_maps()

	def is_valid(self) -> bool:
		return (self.opponent1 and self.opponent2) or self.template

	def get_maps(self):
		pass