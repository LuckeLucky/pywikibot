from typing import List
from ..commons.map import Map as commonsMap

SKIP = 'skip'

class Map(commonsMap):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Map', indent = '', end = '}}')

	def __str__(self) -> str:
		playedMap = self.getValue(self.prefix)
		winner = self.getValue(self.prefix + 'win')
		if not winner and playedMap:
			winner = SKIP

		out = [
			('map', playedMap),
			('mode', self.getValue(self.prefix + 'type'), True)
		]

		score = self.getValue(self.prefix + 'score')
		if score and '-' in score:
			splitScore = score.split('-', 1)
			out.extend([
				('score1', splitScore[0]),
				('score2', splitScore[1])
			])
		out.extend([
			('winner', winner),
			('vod', self.getValue('vodgame' + str(self.index)))
		])

		return self.generateString([out])
