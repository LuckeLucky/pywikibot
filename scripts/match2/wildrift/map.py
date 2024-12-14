from typing import List
from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Map\n        ', indent = '        ', end = '    }}')

	def __str__(self) -> str:
		out = [
			('vod', self.getValue('vod')),
			[
				('team1side', self.getValue('team1side')),
				('team2side', self.getValue('team2side')),
				('length', self.getValue('length')),
				('winner', self.getValue('win')),
			],
			self.getFoundPrefix('t1c'),
			self.getFoundPrefix('t2c'),
			self.getFoundPrefix('t1b'),
			self.getFoundPrefix('t2b'),
		]

		return self.generateString(out)