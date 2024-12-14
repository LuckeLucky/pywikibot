from ..commons.template import Template
from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 10
WILDRIFT_PARAMS = STREAMS + [
	'walkover',
	'vod',
	'mvp',
	'mvppoints',
	'reddit',
	'bestgg',
	'review',
	'recap'
]

class Match(commonsMatch):
	def getMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			mapTemplate = self.template.getNestedTemplate('match' + str(mapIndex))
			if mapTemplate is None:
				mapTemplate = self.template.createFakeTemplate()
			mapTemplate.add('win', mapTemplate.get('win') if mapTemplate.get('win') else self.getValue('map' + str(mapIndex) + 'win'))
			mapTemplate.add('vod', mapTemplate.get('vod') if mapTemplate.get('vod') else self.getValue('vodgame' + str(mapIndex)))
			if not mapTemplate.get('win'):
				break
			self.maps.append(Map(mapIndex, mapTemplate))

	def __str__(self) -> str:
		out = [
			('bestof', self.getValue('bestof')),
			[('date', self.getValue('date')), ('finished', self.getValue('finished'))],
			('winner', self.getValue('winner'), True),
			('opponent1', str(self.opponents[0])),
			('opponent2', str(self.opponents[1])),
		]
		out.extend(self.getFoundMatches(WILDRIFT_PARAMS))

		for matchMap in self.maps:
			out.append(('map' + str(matchMap.index), str(matchMap)))

		location = self.getValue('location')
		comment = self.getValue('comment')
		if location:
			if comment:
				comment = comment + '<br/>' + location
			else:
				comment = location
		if comment:
			out.append(('comment', comment))

		return self.generateString(out)
