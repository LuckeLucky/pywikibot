from mwparserfromhell.nodes import Template

from .opponent import Opponent
from .utils import *

class Match(object):
	def __init__(self, opponent1: Opponent, opponent2: Opponent, winner: int, template: Template, is_reset: bool) -> None:
		self.opponent1 = opponent1
		self.opponent2 = opponent2
		self.template = sanitize_template(template)
		self.data = template_parameters_to_str_dict(template)
		self.maps = []

		self.get_maps()

	def is_valid(self) -> bool:
		return (self.opponent1 and self.opponent2) or self.template
	
	def is_reset(self) -> bool:
		return self.is_reset

	def get_maps(self):
		pass