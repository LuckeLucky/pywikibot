import io

from mwparserfromhell.nodes import Template

from scripts.match2.commons.opponent import Opponent
from scripts.match2.commons.utils import Template

from ..commons.utils import *
from ..commons.match import Match, STREAMS

from .map import Map, MAP_LINKS

CS_PARAMS = STREAMS + [
	'comment',
	'overturned',
	'nostats',
	'nosides',
	'preview',
	'lrthread',
	'cevo',
	'cevo2',
	'sltv',
	'sltv-e',
	'lpl',
	'epiclan',
	'pinger',
	'99damage',
	'99liga',
	'5eplay',
	'draft5',
	'hltvlegacy',
	'hltv',
	'hltv2'
]

class Match(Match):
	def __init__(self, opponent1: Opponent, opponent2: Opponent, template: Template) -> None:
		super().__init__(opponent1, opponent2, template)
		""" self.out = None
		self.out = str(self) """

	def get_maps(self):
		index = 1
		while(True):
			strIndex = str(index)
			mapX = get_parameter_str(self.template, 'map' + strIndex)
			if mapX:
				self.maps.append(Map(index, self.template))
			else:
				break
			index += 1

	def __str__(self) -> str:
		""" if self.out:
			return self.out """
		indent = "\t"
		out = ("{{Match\n" +
			f"{indent}|opponent1={str(self.opponent1)}\n" +
			f"{indent}|opponent2={str(self.opponent2)}\n" +
			f"{indent}|date={get_value_or_empty(self.data, 'date')}"
			f"{indent}|finished={get_value_or_empty(self.data, 'finished')}\n"
		)
		winner = get_value_or_empty(self.data, 'winner')
		if winner:
			out += f"{indent}|winner={winner}\n"

		for key in KeysInDictionaryIterator(CS_PARAMS, self.data):
			out += f"{indent}|{key}={self.data[key]}\n"

		for key in KeysInDictionaryIterator(MAP_LINKS, self.data):
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