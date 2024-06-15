from ..commons.template import Template
from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 10
WILDRIFT_PARAMS = STREAMS + [
	'walkover',
	'vod',
	'mvp',
	'mvppoints',
	'preview',
	'lrthread',
	'reddit',
	'bestgg',
	'interview',
	'review',
	'recap'
]

class Match(commonsMatch):
	def getMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			mapTemplate = self.template.getNestedTemplate('match' + str(mapIndex))
			mapWinner = self.getValue('map' + str(mapIndex) + 'win')
			mapVod = self.getValue('vodgame' + str(mapIndex))
			if mapTemplate is None and (mapWinner or mapVod):
				mapTemplate = Template.createFakeTemplate()
			if not mapTemplate:
				break
			mapTemplate = Template(mapTemplate)
			if not mapTemplate.getValue('win'):
				mapTemplate.add('win', mapWinner)
			if not mapTemplate.getValue('vod'):
				mapTemplate.add('vod', mapVod)
			newMap = Map(mapIndex, mapTemplate)
			self.maps.append(newMap)

	def __str__(self) -> str:
		indent = self.indent
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		out = ("{{Match\n" +
		 	f"{indent}|bestof={self.getValue('bestof')}\n" +
			f"{indent}|date={self.getValue('date')}" +
			f" |finished={self.getValue('finished')}\n"
		)
		winner = self.getValue('winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		streamsParams = ""
		for key, value in self.template.iterateByItemsMatch(WILDRIFT_PARAMS):
			streamsParams += f"|{key}={value}"
		if streamsParams:
			out += indent + streamsParams + "\n"

		out = (
			out +
			f"{indent}|opponent1={str(opponent1)}\n" +
			f"{indent}|opponent2={str(opponent2)}\n"
		)

		for matchMap in self.maps:
			index = matchMap.index
			out += f"{indent}|map{index}={str(matchMap)}\n"

		location = self.getValue('location')
		comment = self.getValue('comment')
		if location:
			if comment:
				comment = comment + '<br/>' + location
			else:
				comment = location
		if comment:
			out += f"{indent}|comment={comment}\n"

		out += "}}"
		return out
