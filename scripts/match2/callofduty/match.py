from typing import List

from scripts.match2.commons.opponent import Opponent
from scripts.match2.commons.template import Template

from ..commons.match import Match as commonsMatch, STREAMS
from ..commons.mapveto import MapVeto

from .map import Map

MAX_NUMBER_OF_MAPS = 20
COD_PARAMS = STREAMS + [
	'bestof'
	'walkover',
	'comment',
	'vod',
	'mvp',
	'mvppoints',
]

class Match(commonsMatch):
	def __init__(self, opponents: List[Opponent], template: Template) -> None:
		super().__init__(opponents, template)
		mapbans = self.template.getNestedTemplate('mapbans')
		self.mapveto = None
		if mapbans:
			self.mapveto = MapVeto(mapbans)

	def populateMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			mapName = self.getValue('map' + str(mapIndex))
			if mapName:
				newMap = Map(mapIndex, self.template)
				self.maps.append(newMap)
			else:
				break

	def __str__(self) -> str:
		out = [
			[('date', self.getValue('date')), ('finished', self.getValue('finished'))],
			('winner', self.getValue('winner'), True),
		]
		out.extend(self.getFoundMatches(COD_PARAMS))
		out.extend([
			('opponent1', str(self.opponents[0])),
			('opponent2', str(self.opponents[1])),
		])

		for matchMap in self.maps:
			out.append(('map' + str(matchMap.index), str(matchMap)))

		return self.generateString(out)
