from scripts.match2.commons.template import Template

from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 10
OVERWATCH_PARAMS = STREAMS + [
	'comment',
	'walkover',
	'vod',
	'mvp',
	'mvppoints',
]

class Match(commonsMatch):
	def getMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			prefix = 'map' + str(mapIndex)
			mapTemplate = self.template.getNestedTemplate('match' + str(mapIndex))
			if not mapTemplate:
				mapTemplate = Template.initFromDict('Fake', {
					'map': self.getValue(prefix),
					'win': self.getValue(prefix + 'win'),
					'score': self.getValue(prefix + 'score'),
					'vod': self.getValue('vodgame' + str(mapIndex))
				})
			if not mapTemplate.get('map'):
				break
			self.maps.append(Map(mapIndex, mapTemplate))

	def __str__(self) -> str:
		out = [
			[('date', self.getValue('date')), ('finished', self.getValue('finished'))],
			('opponent1', str(self.opponents[0])),
			('opponent2', str(self.opponents[1])),
			('winner', self.getValue('winner'), True),
		]
		out.extend(self.getFoundMatches(OVERWATCH_PARAMS))

		for matchMap in self.maps:
			out.append(('map' + str(matchMap.index), str(matchMap)))

		return self.generateString(out)
