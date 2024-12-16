from typing import List
from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Map\n        ', indent = '        ', end = '    }}')

	def __str__(self) -> str:
		out = [
			('team1side', self.getValue('team1side')),
			self.getFoundPrefix('t1c'),
			self.getFoundPrefix('t1b'),
			('team2side', self.getValue('team2side')),
			self.getFoundPrefix('t2c'),
			self.getFoundPrefix('t2b'),
			[('length', self.getValue('length')), ('winner', self.getValue('win'))]
		]

		return self.generateString(out)