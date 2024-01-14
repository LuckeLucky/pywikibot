import io
from typing import List

from scripts.match2.commons.opponent import Opponent
from scripts.match2.commons.template import Template

from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map, MAP_LINKS

CS_PARAMS = STREAMS + [
	'comment',
	'overturned',
	'nostats',
	'nosides',
	'preview',
	'lrthread',
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
	def __init__(self, opponents: List[Opponent], template: Template) -> None:
		super().__init__(opponents, template)
		self.indent = '\t'

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
		indent = self.indent
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		out = ("{{Match\n" +
			f"{indent}|opponent1={str(opponent1)}\n" +
			f"{indent}|opponent2={str(opponent2)}\n" +
			f"{indent}|date={self.template.getValue('date')}"
			f" |finished={self.template.getValue('finished')}\n"
		)
		winner = self.template.getValue('winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		for key, value in self.template.iterateByItemsMatch(CS_PARAMS):
			out += f"{indent}|{key}={value}\n"

		for key, value in self.template.iterateByItemsMatch(MAP_LINKS):
			out += f"{indent}|{key}={value}\n"

		for matchMap in self.maps:
			index = matchMap.index
			mapsOut = f"{indent}|map{index}={str(matchMap)}\n"
			for line in io.StringIO(mapsOut):
				if line.startswith(indent) and ('{{' not in line) and ('}}' not in line):
					out += indent + line
				else:
					out += line

		out += "}}"
		return out
