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
	def getMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			mapTemplate = self.template.getNestedTemplate('match' + str(mapIndex))
			valid = self.template.getfirstValueFound([
				'vodgame' + str(mapIndex),
				'map' + str(mapIndex) + 'win',
				'map' + str(mapIndex) + 'score'
			])
			if mapTemplate:
				mapTemplate.add('vodgame' + str(mapIndex), self.getValue('vodgame' + str(mapIndex)))
				newMap = Map(mapIndex, Template(mapTemplate))
				self.maps.append(newMap)
			elif valid:
				newMap = Map(mapIndex, self.template)
				self.maps.append(newMap)

	def __str__(self) -> str:
		out = [
			self.printParam('bestof', end= '\n', ignoreIfEmpty=True),
			self.printParam('date', end = self.printParam('finished', end = '\n')),
			self.printParam('winner', ignoreIfEmpty=True, end = '\n'),
			self.printMatch(STREAMS, ignoreIfResultEmpty=True, end= '\n'),
			f'|opponent1={str(self.opponents[0])}' + '\n',
			f'|opponent2={str(self.opponents[1])}' + '\n',
			self.printMatch(POKEMON_PARAMS, end= '\n', ignoreIfResultEmpty=True)
		]

		for matchMap in self.maps:
			out.append(f'|map{matchMap.index}={str(matchMap)}\n')

		return self.print(out)
