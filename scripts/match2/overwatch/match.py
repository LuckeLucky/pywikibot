from scripts.match2.commons.template import Template

from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 10
OVERWATCH_PARAMS = STREAMS + [
	'comment',
	'walkover',
	'vod',
	'mvp',
	'mvppoints',
	'owl',
	'owc',
	'jcg',
	'pllg',
	'oceow',
	'tespa',
	'overgg',
	'pf',
	'wl',
	'review',
	'recap'
]

class Match(commonsMatch):
	def getMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			mapName = self.getValue('map' + str(mapIndex))
			mapTemplate = self.template.getNestedTemplate('match' + str(mapIndex))
			mapVod = self.getValue('vodgame' + str(mapIndex))
			if mapName:
				newMap = Map(mapIndex, self.template)
				self.maps.append(newMap)
			elif mapTemplate:
				mapTemplate.add('vodgame' + str(mapIndex), mapVod)
				newMap = Map(mapIndex, Template(mapTemplate))
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
			f"{indent}|opponent1={str(opponent1)}\n" +
			f"{indent}|opponent2={str(opponent2)}\n"
		)
		winner = self.getValue('winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		for key, value in self.template.iterateByItemsMatch(OVERWATCH_PARAMS):
			out += f"{indent}|{key}={value}\n"

		for matchMap in self.maps:
			index = matchMap.index
			out += f"{indent}|map{index}={str(matchMap)}\n"

		out += "}}"
		return out
