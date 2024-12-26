from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 100

class Match(commonsMatch):
	def getMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			if any(val[1] != '' for val in self.getFoundPrefix(f'g{mapIndex}')):
				newMap = Map(mapIndex, self.template)
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
