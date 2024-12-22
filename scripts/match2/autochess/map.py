from typing import List
from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Map', indent = '', end = '}}')

	def __str__(self) -> str:
		return self.generateString([
			('winner', self.getValue('winner'))
		])
