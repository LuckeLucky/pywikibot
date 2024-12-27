from typing import List
from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 100

PALADINS_PARAMS = STREAMS + [
	'mvp'
]

class Match(commonsMatch):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params,
			templateId = 'Match2\n    ',
			indent = '    ',
			end = '}}'
		)

	def populateMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			if self.getValue('match' + str(mapIndex)):
				for key, value in self.getValue('match' + str(mapIndex)).iterateParams():
					newKey = 'map' + str(mapIndex) + key
					if not self.getValue(newKey):
						self.template.add(newKey, value)
			prefixed = self.getFoundPrefix('map' + str(mapIndex))
			if any(val[1] != '' for val in prefixed):
				newMap = Map(mapIndex, self.template)
				self.maps.append(newMap)
			else:
				break

	def __str__(self) -> str:
		out = [
			('opponent1', str(self.opponents[0])),
			('opponent2', str(self.opponents[1])),
			[('date', self.getValue('date')), ('finished', self.getValue('finished'))],
			self.getFoundMatches(PALADINS_PARAMS),
			('vod', self.getValue('vod'), True),
			('comment', self.getValue('comment'), True)
		]

		for matchMap in self.maps:
			out.append(('map' + str(matchMap.index), str(matchMap)))

		return self.generateString(out)
