import io

from ..commons.template import Template
from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

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
		index = 1
		while True:
			strIndex = str(index)
			mapTemplate = self.template.getNestedTemplate('match' + strIndex)
			mapTemplate = Template(mapTemplate)
			#Winner outside of MatchLua
			mapWinner = mapTemplate.getValue('map' + strIndex + 'win')
			if mapTemplate is None and mapWinner:
				mapTemplate = Template.createFakeTemplate()
			if not mapTemplate:
				break
			if not mapTemplate.getValue(mapTemplate, 'win'):
				mapTemplate.add('win', mapWinner)
			self.maps.append(Map(index, mapTemplate))
			index += 1

	def __str__(self) -> str:
		indent = "  "
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
			mapsOut = f"{indent}|map{index}={str(matchMap)}\n"
			for line in io.StringIO(mapsOut):
				if line.startswith(indent) and ('{{' not in line) and ('}}' not in line):
					out += indent + line
				else:
					out += line

		out += "}}"
		return out
