from ..commons.template import Template
from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 10
DOTA_PARAMS = STREAMS + [
	'comment',
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
	'recap',
	'replay'
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
			if not mapTemplate.getValue('win'):
				mapTemplate.add('win', mapWinner)
			newMap = Map(mapIndex, mapTemplate)
			self.maps.append(newMap)

	def __str__(self) -> str:
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		out = ("{{Match2\n" +
			f"|opponent1={str(opponent1)}\n" +
			f"|opponent2={str(opponent2)}\n" +
			f"|date={self.template.getValue('date')}\n"
			f"|finished={self.template.getValue('finished')}\n")

		winner = self.template.getValue('winner')
		if winner:
			out += f"|winner={winner}\n"

		for key, value in self.template.iterateByItemsMatch(DOTA_PARAMS):
			out += f"|{key}={value}\n"

		for key, value in self.template.iterateByPrefix('vodgame', ignoreEmpty=True):
			out += f"|{key}={value}\n"

		for key, value in self.template.iterateByPrefix('matchid'):
			out += f"|{key}={value}\n"

		for matchMap in self.maps:
			index = matchMap.index
			out += f"|map{index}={str(matchMap)}\n"

		out += "}}"

		return out
