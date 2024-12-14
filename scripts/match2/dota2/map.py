from typing import List
from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Map\n', indent = '', end = '}}')

	def getPrefixedParams(self, prefix: str) -> List:
		result = self.getFoundPrefix(prefix)
		
		for key, value in self.template.iterateByPrefix(prefix):
			result += f"|{key}={value}"
		return result

	def __str__(self) -> str:
		out = [
			('team1side', self.getValue('team1side')),
			self.getPrefixedParams('t1h'),
			self.getPrefixedParams('t1b'),
			('team2side', self.getValue('team2side')),
			self.getPrefixedParams('t2h'),
			self.getPrefixedParams('t2b'),
			[('length', self.getValue('length')), ('winner', self.getValue('win'))]
		]

		return self.generateString(out)
