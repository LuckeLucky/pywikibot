from typing import List

from scripts.match2.commons.map import Map as commonsMap

SKIP = 'skip'

class Map(commonsMap):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Map', indent = '', end = '}}')

	def __str__(self) -> str:
		out = [
			('date', self.getValue('date')),
			('finished', self.getValue('finished')),
			('map', self.getValue('map')),
			('vod', self.getValue('vod')),
			('stats', self.getValue('stats'))
		]

		return self.generateString([out])
