from typing import List

from scripts.match2.commons.opponent import Opponent
from ..commons.template import Template
from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 10

class Match(commonsMatch):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Match', indent = '    ', end = '}}')

	def __init__(self, opponents: List[Opponent], template: Template) -> None:
		super().__init__(opponents, template)
		if self.template._name == 'BracketMatchSummary1':
			self.template.add('hasSubmatches', '1')

	def populateMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			prefix = 'map' + str(mapIndex)
			mapTemplate = self.template.getNestedTemplate('match' + str(mapIndex))
			if mapTemplate:
				for key, value in mapTemplate.iterateParams():
					self.template.add(prefix + key, value)
			else:
				if not self.template.has(prefix):
					break

			self.maps.append(Map(mapIndex, self.template))

	def __str__(self) -> str:
		out = [
			('finished', self.getValue('finished')),
			('bestof', self.getValue('bestof')),
			('hasSubmatches', '1', True),
			('winner', self.getValue('winner')),
			('date', self.getValue('date')),
			self.getFoundMatches(STREAMS),
			('opponent1', str(self.opponents[0])),
			('opponent2', str(self.opponents[1])),
			('comment', self.getValue('comment'), True)
		]

		for matchMap in self.maps:
			out.append(('map' + str(matchMap.index), str(matchMap)))

		return self.generateString(out)