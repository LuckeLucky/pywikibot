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
			mapVeto = MapVeto(Template(mapbans))
			self.mapveto = mapVeto

	def getMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			mapName = self.getValue('map' + str(mapIndex))
			if mapName:
				newMap = Map(mapIndex, self.template)
				self.maps.append(newMap)
			else:
				break

	def __str__(self) -> str:
		indent = self.indent
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		out = ("{{Match\n" +
			f"{indent}|date={self.getValue('date')}" +
			f" |finished={self.getValue('finished')}\n"
		)
		winner = self.getValue('winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		for key, value in self.template.iterateByItemsMatch(COD_PARAMS):
			out += f"{indent}|{key}={value}\n"

		out = (
			out +
			f"{indent}|opponent1={str(opponent1)}\n" +
			f"{indent}|opponent2={str(opponent2)}\n"
		)

		for matchMap in self.maps:
			index = matchMap.index
			out += f"{indent}|map{index}={str(matchMap)}\n"

		out += "}}"
		return out
