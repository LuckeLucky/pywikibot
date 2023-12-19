import io
from mwparserfromhell.nodes import Template

from ..commons.utils import *
from ..commons.match import Match, STREAMS

from .map import Map

LEAGUE_PARAMS = STREAMS + [
	'walkover',
	'vod',
	'comment',
	'location',
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

class Match(Match):
	def getMaps(self):
		index = 1
		while(True):
			strIndex = str(index)
			match_template = getNestedTemplateFromTemplate(self.template, 'match' + strIndex)
			#Winner outside of MatchLua
			winner = getValueOrEmpty(self.data, 'map' + strIndex + 'winner')
			if match_template is None and winner:
				match_template = Template('MatchLua')
				match_template.add('win', winner)
			elif not getStringFromTemplate(match_template, 'win') and winner:
				match_template.add('win', winner)
			if match_template is None:
				break
			self.maps.append(Map(index, match_template))
			index += 1

	def __str__(self) -> str:
		indent = "  "
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		out = ("{{Match2\n" +
			f"{indent}|opponent1={str(opponent1)}\n" +
			f"{indent}|opponent2={str(opponent2)}\n" +
			f"{indent}|date={getValueOrEmpty(self.data, 'date')}"
			f"{indent}|finished={getValueOrEmpty(self.data, 'finished')}\n"
		)
		winner = getValueOrEmpty(self.data, 'winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		for key in KeysInDictionaryIterator(LEAGUE_PARAMS, self.data):
			out += f"{indent}|{key}={self.data[key]}\n"
			
		for key in PrefixIterator('vodgame', self.data):
			out += f"{indent}|{key}={self.data[key]}\n"

		for key in PrefixIterator('matchhistory', self.data):
			out += f"{indent}|{key}={self.data[key]}\n"

		for map in self.maps:
			index = map.index
			maps_out = f"{indent}|map{index}={str(map)}\n"
			for line in io.StringIO(maps_out):
				if line.startswith(indent) and ('{{' not in line) and ('}}' not in line):
					out += indent + line
				else:
					out += line

		out += "}}"
		return out