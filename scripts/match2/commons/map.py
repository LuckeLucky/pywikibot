from mwparserfromhell.nodes import Template
from .utils import getTemplateParameters, sanitizeTemplate

class Map:
	def __init__(self, index: int, template: Template) -> None:
		self.index = index
		self.data = getTemplateParameters(sanitizeTemplate(template))
