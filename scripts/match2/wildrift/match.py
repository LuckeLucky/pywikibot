import io
from ..commons.template import Template
from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

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
		index = 1
		while True:
			strIndex = str(index)
			mapTemplate = self.template.getNestedTemplate('match' + strIndex)
			#Winner outside of MatchLua
			mapWinner = self.template.getValue('map' + strIndex + 'win')
			mapVod = self.template.getValue('vodgame' + strIndex)
			if mapTemplate is None and (mapWinner or mapVod):
				mapTemplate = Template.createFakeTemplate()
			if not mapTemplate:
				break
			mapTemplate = Template(mapTemplate)
			if not mapTemplate.getValue('win'):
				mapTemplate.add('win', mapWinner)
			if not mapTemplate.getValue('vod'):
				mapTemplate.add('vod', mapVod)
			self.maps.append(Map(index, mapTemplate))
			index += 1

	def __str__(self) -> str:
		indent = "    "
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		out = ("{{Match\n" +
		 	f"{indent}|bestof={self.template.getValue('bestof')}\n" +
			f"{indent}|date={self.template.getValue('date')}" +
			f" |finished={self.template.getValue('finished')}\n"
		)
		winner = self.template.getValue('winner')
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
			mapsOut = f"{indent}|map{index}={str(matchMap)}\n"
			for line in io.StringIO(mapsOut):
				if ('{{' not in line) and ('}}' not in line):
					out += indent + line
				else:
					out += line

		location = self.template.getValue('location')
		comment = self.template.getValue('comment')
		if location:
			if comment:
				comment = comment + '<br/>' + location
			else:
				comment = location
		if comment:
			out += f"{indent}|comment={comment}\n"

		out += "}}"
		return out
