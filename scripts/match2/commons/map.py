from mwparserfromhell.nodes import Template
from .utils import *

class Map(object):
	def __init__(self, index: int, template: Template) -> None:
		self.index = index
		self.data = template_parameters_to_str_dict(sanitize_template(template))