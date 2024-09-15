from typing import List
from .template import Template
from .templateutils import TemplateUtils
class Map(TemplateUtils):
	def __init__(self, index: int, template: Template) -> None:
		self.indent = '        '
		self.index = index
		self.prefix = 'map' + str(self.index)
		super().__init__(template)

	def print(self, params: List[str]) -> str:
		return super().printTemplate(params, templateId = 'Map', indent = '        ', end = '    }}', ignoreEmptyParams = True)
