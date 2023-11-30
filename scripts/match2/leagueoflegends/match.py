import io
from mwparserfromhell.nodes import Template
from scripts.match2.utils import Template

from ..utils import *
from ..match import Match
from ..opponent import Opponent

from .map import Map

STREAMS = [
	'stream',
	'twitch',
	'twitch2',
	'afreeca',
	'afreecatv',
	'dailymotion',
	'douyu',
	'huomao',
	'youtube',
	'facebook',
	'pandatv',
	'huya',
	'bilibili',
	'steamtv',
	'vod',
	'vod2',
	'reddit'
]

class Match(Match):
	def __init__(self, opponent1: Opponent, opponent2: Opponent, winner: int, template: Template, is_reset: bool) -> None:
		super().__init__(opponent1, opponent2, winner, template, is_reset)

	def get_maps(self):
		for key in PrefixIterator('match', self.data):
			match_template = get_parameter_template(self.template, key)
			index = key.replace('match', '')
			#Winner outside of MatchLua
			winner = get_value_or_empty(self.data, 'map' + index + 'winner')
			if match_template is None and winner:
				match_template = Template('MatchLua')
				match_template.add('win', winner)
			elif not get_parameter_str(match_template, 'win') and winner:
				match_template.add('win', winner)

			self.maps.append(Map(int(index), match_template))

	def __str__(self) -> str:
		indent = "  "
		out = ("{{Match2\n" +
			f"{indent}|opponent1={str(self.opponent1)}\n" +
			f"{indent}|opponent2={str(self.opponent2)}\n" +
			f"{indent}|date={get_value_or_empty(self.data, 'date')}\n"
		)
		winner = get_value_or_empty(self.data, 'winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		for key in KeysInDictionaryIterator(STREAMS, self.data):
			out += f"{indent}|{key}={self.data[key]}\n"
			
		for key in PrefixIterator('vodgame', self.data):
			out += f"{indent}|{key}={self.data[key]}\n"

		walkover = get_value_or_empty(self.data, 'walkover')
		if walkover:
			out += f"{indent}|walkover={walkover}\n"

		comment = get_value_or_empty(self.data, 'comment')
		if comment:
			out += f"{indent}!comment={comment}\n"

		for key in PrefixIterator('vodgame', self.data):
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