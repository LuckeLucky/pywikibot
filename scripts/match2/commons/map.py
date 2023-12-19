from mwparserfromhell.nodes import Template
from .utils import *

class Map(object):
	def __init__(self, index: int, template: Template) -> None:
		self.index = index
		self.data = getTemplateParameters(sanitizeTemplate(template))