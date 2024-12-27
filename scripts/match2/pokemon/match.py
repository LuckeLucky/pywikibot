from scripts.match2.commons.template import Template

from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 20
POKEMON_PARAMS = [
	'comment',
	'walkover',
	'vod',
	'mvp',
	'mvppoints',
]

class Match(commonsMatch):
	def populateMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			mapTemplate = self.template.getNestedTemplate('match' + str(mapIndex))
			if mapTemplate:
				mapTemplate.add('vodgame' + str(mapIndex), self.getValue('vodgame' + str(mapIndex)))
				newMap = Map(mapIndex, Template(mapTemplate))
				self.maps.append(newMap)
			elif self.template.getfirstValueFound([
				'vodgame' + str(mapIndex),
				'map' + str(mapIndex) + 'win',
				'map' + str(mapIndex) + 'score'
			]):
				newMap = Map(mapIndex, self.template)
				self.maps.append(newMap)

	def __str__(self) -> str:
		out = [
			('bestof', self.getValue('bestof')),
			('date', self.getValue('date')),
			('finished', self.getValue('finished')),
			('opponent1', str(self.opponents[0])),
			('opponent2', str(self.opponents[1])),
		]
		out.extend(self.getFoundMatches(POKEMON_PARAMS))

		for matchMap in self.maps:
			out.append(('map' + str(matchMap.index), str(matchMap)))

		return self.generateString(out)
