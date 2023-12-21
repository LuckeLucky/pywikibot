import io
from mwparserfromhell.nodes import Template

from ..commons.utils import (
    getNestedTemplateFromTemplate,
    getValueOrEmpty,
    getStringFromTemplate,
    KeysInDictionaryIterator,
    PrefixIterator
)
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
			matchTemplate = getNestedTemplateFromTemplate(self.template, 'match' + strIndex)
			#Winner outside of MatchLua
			winner = getValueOrEmpty(self.data, 'map' + strIndex + 'winner')
			if matchTemplate is None and winner:
				matchTemplate = Template('MatchLua')
				matchTemplate.add('win', winner)
			elif not getStringFromTemplate(matchTemplate, 'win') and winner:
				matchTemplate.add('win', winner)
			if matchTemplate is None:
				break
			self.maps.append(Map(index, matchTemplate))
			index += 1

	def __str__(self) -> str:
		indent = "  "
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		out = ("{{Match2\n" +
			f"{indent}|opponent1={str(opponent1)}\n" +
			f"{indent}|opponent2={str(opponent2)}\n" +
			f"{indent}|date={getValueOrEmpty(self.data, 'date')}"
			f" |finished={getValueOrEmpty(self.data, 'finished')}\n"
		)
		winner = getValueOrEmpty(self.data, 'winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		for key in KeysInDictionaryIterator(LEAGUE_PARAMS, self.data):
			out += f"{indent}|{key}={self.data[key]}\n"

		location = getValueOrEmpty(self.data, 'location')
		comment = getValueOrEmpty(self.data, 'comment')
		if location:
			if comment:
				comment = comment + '<br/>' + location
			else:
				comment = location
		if comment:
			out += f"{indent}|comment={comment}\n"

		for key in PrefixIterator('vodgame', self.data):
			out += f"{indent}|{key}={self.data[key]}\n"

		for key in PrefixIterator('matchhistory', self.data):
			out += f"{indent}|{key}={self.data[key]}\n"

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
