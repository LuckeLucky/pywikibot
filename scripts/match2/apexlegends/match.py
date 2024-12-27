from scripts.match2.commons.match import Match as commonsMatch, STREAMS

from ..commons.template import Template
from .map import Map

class Match(commonsMatch):
	def populateMaps(self) -> None:
		mapIndex = 1
		rounds = int(self.getValue('rounds'))
		streamsDict = Template.initFromDict('test', {})
		for key, mapTemplate in self.template.iterateByPrefix('details'):
			#move streams from map template to matchtemplate
			for streamKey, value in mapTemplate.iterateByItemsMatch(STREAMS, ignoreEmpty=True):
				streamsDict.addIfNotHas(streamKey, value)
			self.maps.append(Map(int(key.replace('details', '')), mapTemplate))
			if rounds == mapIndex:
				break
			mapIndex += 1

		for key, value in streamsDict.iterateParams():
			self.template.addIfNotHas(key, value)

	def __str__(self) -> str:
		itemsMatch = [f'p{i}' for i in range(1, 200)]
		itemsMatch.insert(0, 'p_kill')
		out = [
			('finished', 'true'),
			self.getFoundMatches(itemsMatch) + [('matchpoint', '50')],
			self.getFoundMatches(STREAMS)
		]

		for matchMap in self.maps:
			out.append(('map' + str(matchMap.index), str(matchMap)))

		for opponentIndex, opponent in enumerate(self.opponents):
			out.append((f'opponent{opponentIndex + 1}', str(opponent)))

		return self.generateString(out)
