from ..commons.match import Match as commonsMatch, STREAMS
from ..commons.template import Template

from .map import Map

MAX_NUMBER_OF_MAPS = 100

class Match(commonsMatch):
	def populateMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			key = 'map' + str(mapIndex) + 'win'
			if self.getValue(key):
				newMap = Map(mapIndex, Template.initFromDict('', {
					'winner': self.getValue(key)
				}))
				self.maps.append(newMap)
			else:
				break

	def __str__(self) -> str:
		out = [
			('opponent1', str(self.opponents[0])),
			('opponent2', str(self.opponents[1])),
			[('date', self.getValue('date')), ('finished', self.getValue('finished'))],
			self.getFoundMatches(STREAMS),
			('vod', self.getValue('vod'), True),
			('comment', self.getValue('comment'), True)
		]

		for matchMap in self.maps:
			out.append(('map' + str(matchMap.index), str(matchMap)))

		return self.generateString(out)
