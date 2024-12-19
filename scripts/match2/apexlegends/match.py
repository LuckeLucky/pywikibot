from scripts.match2.commons.match import Match as commonsMatch

from .map import Map

class Match(commonsMatch):
	def getMaps(self) -> None:
		mapIndex = 1
		for _, mapTemplate in self.template.iterateByPrefix('details'):
			if not any(val != '' for _, val in mapTemplate.iterateParams()):
				break
			self.maps.append(Map(mapIndex, mapTemplate))
			mapIndex += 1

	def __str__(self) -> str:
		itemsMatch = [f'p{i}' for i in range(1, 20)]
		itemsMatch.insert(0, 'p_kill')
		out = [
			('finished', 'true'),
			self.getFoundMatches(itemsMatch),
		]

		for matchMap in self.maps:
			out.append(('map' + str(matchMap.index), str(matchMap)))

		for opponentIndex, opponent in enumerate(self.opponents):
			out.append((f'opponent{opponentIndex + 1}', str(opponent)))

		return self.generateString(out)
