from ..commons.template import Template
from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 10
LEAGUE_PARAMS = STREAMS + [
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
			mapWinner = self.template.getValue('map' + str(mapIndex) + 'win')
			if mapTemplate is None and mapWinner:
				mapTemplate = Template.createFakeTemplate()
			if not mapTemplate:
				break
			mapTemplate = Template(mapTemplate)
			if not mapTemplate.getValue(mapTemplate, 'win'):
				mapTemplate.add('win', mapWinner)
			newMap = Map(mapIndex, mapTemplate)
			newMap.indent = self.indent * 2

	def __str__(self) -> str:
		indent = self.indent
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		out = ("{{Match2\n" +
			f"{indent}|opponent1={str(opponent1)}\n" +
			f"{indent}|opponent2={str(opponent2)}\n" +
			f"{indent}|date={self.template.getValue('date')}"
			f" |finished={self.template.getValue('finished')}\n"
		)
		winner = self.template.getValue('winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		for key, value in self.template.iterateByItemsMatch(LEAGUE_PARAMS):
			out += f"{indent}|{key}={value}\n"

		location = self.template.getValue('location')
		comment = self.template.getValue('comment')
		if location:
			if comment:
				comment = comment + '<br/>' + location
			else:
				comment = location
		if comment:
			out += f"{indent}|comment={comment}\n"

		for key, value in self.template.iterateByPrefix('vodgame'):
			out += f"{indent}|{key}={value}\n"

		for key, value in self.template.iterateByPrefix('matchhistory'):
			out += f"{indent}|{key}={value}\n"

		for matchMap in self.maps:
			index = matchMap.index
			out += f"{indent}|map{index}={str(matchMap)}\n"

		out += "}}"
		return out
