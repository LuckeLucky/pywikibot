from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 21
STARCRAFT_PARAMS = STREAMS + [
	'walkover',
	'review',
	'recap',
	'comment',
	'vod'
]

class Match(commonsMatch):
	def getMaps(self):
		lastIndex = 0
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			prefix = 'm' + str(mapIndex)
			mapName = self.template.getfirstValueFound([prefix + 'map', 'map' + str(mapIndex)])
			if mapName:
				self.template.add(prefix, mapName)

			winner = self.template.getfirstValueFound([prefix + 'win', 'win' + str(mapIndex), f'map{mapIndex}win'])
			if winner:
				self.template.add(prefix + 'win', winner)
			score = self.template.getfirstValueFound([prefix + 'p1score', prefix + 'p2score'])
			player = self.template.getfirstValueFound([prefix + 'p1', prefix + 'p2'])
			if mapName or winner or score or player:
				newMap = Map(mapIndex, self.template)
				newMap.prefix = prefix
				self.maps.append(newMap)
				lastIndex = mapIndex
			else:
				break

		hasHeader = False
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS):
			lastIndex = lastIndex + 1
			newKey = f'm{lastIndex}'

			if self.template.getfirstValueFound([f'ace{mapIndex}p1', f'ace{mapIndex}p2']):
				for key, value in self.template.iterateByPrefix('ace1'):
					self.template.add(key.replace('ace1', newKey), value)
				if not hasHeader:
					self.template.add(f'subgroup{lastIndex}header', 'Ace Match')
					hasHeader = True
				newMap = Map(lastIndex, self.template)
				newMap.prefix = newKey
				self.maps.append(newMap)
			else:
				break

	def __str__(self) -> str:
		out = [
			('bestof', self.getValue('bestof'), True),
			[('date', self.getValue('date'), ('finished', self.getValue('finished'), True))],
			('opponent1', str(self.opponents[0])),
			('opponent2', str(self.opponents[1])),
			('winner', self.getValue('winner'), True)
		]
		out.extend(self.getFoundMatches(STARCRAFT_PARAMS))
		out.extend(self.getFoundPrefix('vodgame'))

		for key, value in self.template.iterateByPrefix('veto', ignoreEmpty=True):
			num = key[-1]
			out.append([(key, value), (f'vetoplayer{num}', str(num))])

		for matchMap in self.maps:
			index = matchMap.index
			out.append(f'subgroup{index}header', self.getValue(f'subgroup{index}header', True))
			out.append(('map' + str(index), str(matchMap)))

		return self.generateString(out)
