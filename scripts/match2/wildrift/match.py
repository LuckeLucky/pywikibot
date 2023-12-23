import io
from mwparserfromhell.nodes import Template

from ..commons.utils import (
	sanitizeTemplate,
    getNestedTemplateFromTemplate,
    getValueOrEmpty,
    getStringFromTemplate,
    KeysInDictionaryIterator
)
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
			mapTemplate = getNestedTemplateFromTemplate(self.template, 'match' + strIndex)
			mapTemplate = sanitizeTemplate(mapTemplate)
			#Winner outside of MatchLua
			mapWinner = getValueOrEmpty(self.data, 'map' + strIndex + 'win')
			mapVod = getValueOrEmpty(self.data, 'vodgame' + strIndex)
			if mapTemplate is None and (mapWinner or mapVod):
				mapTemplate = Template("FAKE")
			if not mapTemplate:
				break
			if not getStringFromTemplate(mapTemplate, 'win'):
				mapTemplate.add('win', mapWinner)
			if not getNestedTemplateFromTemplate(mapTemplate, 'vod'):
				mapTemplate.add('vod', mapVod)
			self.maps.append(Map(index, mapTemplate))
			index += 1

	def __str__(self) -> str:
		indent = "    "
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		out = ("{{Match\n" +
		 	f"{indent}|bestof={getValueOrEmpty(self.data, 'bestof')}\n" +
			f"{indent}|date={getValueOrEmpty(self.data, 'date')}" +
			f" |finished={getValueOrEmpty(self.data, 'finished')}\n"
		)
		winner = getValueOrEmpty(self.data, 'winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		streamsParams = ""
		for key in KeysInDictionaryIterator(WILDRIFT_PARAMS, self.data):
			streamsParams += f"|{key}={self.data[key]}"
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
				if line.startswith(indent) and ('{{' not in line) and ('}}' not in line):
					out += indent + line
				else:
					out += line

		location = getValueOrEmpty(self.data, 'location')
		comment = getValueOrEmpty(self.data, 'comment')
		if location:
			if comment:
				comment = comment + '<br/>' + location
			else:
				comment = location
		if comment:
			out += f"{indent}|comment={comment}\n"

		out += "}}"
		return out
