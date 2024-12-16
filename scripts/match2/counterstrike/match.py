from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map, MAP_LINKS

MAX_NUMBER_OF_MAPS = 10
CS_PARAMS = STREAMS + [
	'comment',
	'overturned',
	'nostats',
	'nosides',
	'cevo',
	'cevo2',
	'sltv',
	'sltv-e',
	'lpl',
	'epiclan',
	'pinger',
	'99damage',
	'99liga',
	'5eplay',
	'draft5',
	'hltvlegacy',
	'hltv',
	'hltv2'
]

class Match(commonsMatch):
	def getMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			mapName = self.getValue('map' + str(mapIndex))
			if mapName:
				newMap = Map(mapIndex, self.template)
				self.maps.append(newMap)
			else:
				break

	def __str__(self) -> str:
		out = [
			('opponent1', str(self.opponents[0])),
			('opponent2', str(self.opponents[1])),
			[('date', self.getValue('date')), ('finished', self.getValue('finished'))],
			('winner', self.getValue('winner'), True),
		]
		out.extend(self.getFoundMatches(CS_PARAMS))
		out.extend(self.getFoundMatches(MAP_LINKS))

		for matchMap in self.maps:
			out.append(('map' + str(matchMap.index), str(matchMap)))

		return self.generateString(out)
