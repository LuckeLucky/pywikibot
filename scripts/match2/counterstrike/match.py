from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map, MAP_LINKS

MAX_NUMBER_OF_MAPS = 10
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
	def getMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			mapName = self.template.getValue('map' + str(mapIndex))
			if mapName:
				newMap = Map(mapIndex, self.template)
				print(newMap.indent)
				self.maps.append(newMap)
			else:
				break

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
			out += f"{indent}|map{index}={str(matchMap)}\n"

		out += "}}"
		return out
