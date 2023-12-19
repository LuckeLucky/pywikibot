from typing import List
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
	def __init__(self, opponents: List[Opponent], template: Template) -> None:
		self.opponents = opponents
		self.template = sanitize_template(template)
		self.data = template_parameters_to_str_dict(self.template)
		self.maps = []

		self.get_maps()

	def is_valid(self) -> bool:
		return (self.opponents[0] and self.opponents[1]) or self.template

	def get_maps(self):
		pass