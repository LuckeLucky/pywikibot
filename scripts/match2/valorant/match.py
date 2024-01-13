import io

from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

VALORANT_PARAMS = STREAMS + [
	'comment',
	'vod',
	'mvp',
	'mvppoints',
	'vlr',
]

class Match(commonsMatch):
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

		out += "}}"
		return out