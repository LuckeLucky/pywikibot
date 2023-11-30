from mwparserfromhell.nodes import Template
from utils import *

class Map(object):
	def __init__(self, index: int, template: Template) -> None:
		self.index = index
		self.data = {}

		sanitized_template = sanitize_template(template)
		for parameter in sanitized_template.params:
			key = str(parameter.name)
			self.data[key] = str(parameter.value)