from typing import List

from scripts.match2.commons.opponent import Opponent
from scripts.match2.commons.template import Template

from ..commons.match import Match as commonsMatch, STREAMS
from ..commons.mapveto import MapVeto

from .map import Map

VALORANT_PARAMS = STREAMS + [
	'bestof'
	'comment',
	'vod',
	'mvp',
	'mvppoints',
	'vlr',
]

class Match(commonsMatch):
	def __init__(self, opponents: List[Opponent], template: Template) -> None:
		super().__init__(opponents, template)
		mapbans = self.template.getNestedTemplate('mapbans')
		if mapbans:
			self.mapveto = MapVeto(Template(mapbans))

	def getMaps(self):
		index = 1
		while True:
			strIndex = str(index)
			mapX = self.template.getValue('map' + strIndex)
			if mapX:
				self.maps.append(Map(index, self.template))
			else:
				break
			index += 1

	def __str__(self) -> str:
		indent = "  "
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		out = ("{{Match\n" +
		 	f"{indent}|date={self.template.getValue('date')}" +
			f" |finished={self.template.getValue('finished')}\n"
			f"{indent}|opponent1={str(opponent1)}\n" +
			f"{indent}|opponent2={str(opponent2)}\n"
		)
		winner = self.template.getValue('winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		for key, value in self.template.iterateByItemsMatch(VALORANT_PARAMS):
			out += f"{indent}|{key}={value}\n"

		for matchMap in self.maps:
			index = matchMap.index
			mapsOut = f"{indent}|map{index}={str(matchMap)}\n"
			splitLines = mapsOut.splitlines(keepends=True)
			out += splitLines[0]
			out += ''.join(indent + line for line in splitLines[1:-1])
			out += splitLines[-1]

		if self.mapveto:
			vetoOut = f'{indent}|mapveto={str(self.mapveto)}\n'
			splitLines = vetoOut.splitlines(keepends=True)
			out += splitLines[0]
			out += ''.join(indent + line for line in splitLines[1:-1])
			out += splitLines[-1]

		out += "}}"
		return out
