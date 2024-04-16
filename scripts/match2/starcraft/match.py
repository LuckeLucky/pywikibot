from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 21
STARCRAFT_PARAMS = STREAMS + [
	'bestof',
	'review',
	'lrthread',
	'preview',
	'interview',
	'recap',
	'comment',
	'vod'
]

class Match(commonsMatch):
	def getMaps(self):
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			prefix = 'map'
			mapName = self.template.getValue(prefix + str(mapIndex))
			winner = self.template.getValue(prefix + 'win')
			if self.template.name in ['FTeamMatch', 'BracketTeamMatch', 'Proleague06Match', 'Proleague04-05Match']:
				prefix = 'm'
				mapName = self.template.getValue('m' + str(mapIndex) + 'map')
				if mapName:
					self.template.remove('m' + str(mapIndex) + 'map')
					self.template.add('m' + str(mapIndex), mapName)
				winner = self.template.getValue('m' + str(mapIndex) + 'win')
			if mapName or winner:
				newMap = Map(mapIndex, self.template)
				newMap.prefix = prefix + str(mapIndex)
				self.maps.append(newMap)
			else:
				break

	def __str__(self) -> str:
		indent = self.indent
		opponent1 = self.opponents[0]
		opponent2 = self.opponents[1]
		out = ('{{Match\n' +
		 	f'{indent}|date={self.template.getValue('date')}' +
			(f'|finished={self.template.getValue('finished')}\n' if self.template.getValue('finished') else '\n') +
			f'{indent}|opponent1={str(opponent1)}\n' +
			f'{indent}|opponent2={str(opponent2)}\n'
		)

		winner = self.template.getValue('winner')
		if winner and not self.template.getValue('bestof'):
			out += f'{indent}|winner={winner}\n'

		for key, value in self.template.iterateByItemsMatch(STARCRAFT_PARAMS):
			out += f"{indent}|{key}={value}\n"

		for key, value in self.template.iterateByPrefix('vodgame'):
			out += f"{indent}|{key}={value}\n"

		for matchMap in self.maps:
			index = matchMap.index
			out += f"{indent}|map{index}={str(matchMap)}\n"

		out += "}}"
		return out
