from typing import List

from scripts.match2.commons.opponent import Opponent
from ..commons.template import Template
from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 10

class Match(commonsMatch):
	def __init__(self, opponents: List[Opponent], template: Template) -> None:
		super().__init__(opponents, template)
		if self.template.name == 'BracketMatchSummary1':
			self.template.add('hasSubmatches', '1')

	def getMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			prefix = 'map' + str(mapIndex)
			mapTemplate = self.template.getNestedTemplate('match' + str(mapIndex))
			if mapTemplate:
				t = Template(mapTemplate)
				for key, value in t.iterateParams():
					self.template.add(prefix + key, value)
			else:
				if not self.template.has(prefix):
					break

			self.maps.append(Map(mapIndex, self.template))

	def __str__(self) -> str:
		indent = self.indent
		out = (
			'{{Match' +
			f'|finished={self.template.getValue('finished')}\n'
		)

		if self.template.getValue('hasSubmatches'):
			out += f'{indent}|hasSubmatches=1\n'

		out = (
			out +
			f"{indent}|winner={self.template.getValue('winner')}\n" +
			f"{indent}|date={self.template.getValue('date')}\n"
		)

		streams = ''
		for key, value in self.template.iterateByItemsMatch(STREAMS):
			streams += f"|{key}={value}"
		if streams:
			out += indent + streams + '\n'

		out = (
			out +
			f"{indent}|opponent1={str(self.opponents[0])}\n" +
			f"{indent}|opponent2={str(self.opponents[1])}\n"
		)

		for matchMap in self.maps:
			index = matchMap.index
			out += f"{indent}|map{index}={str(matchMap)}\n"

		out += "}}"
		return out
