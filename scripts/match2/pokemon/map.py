from typing import List
from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Map', indent = '', end = '}}')

	def __str__(self) -> str:
		out = []
		score = self.getValue(self.prefix + 'score')
		if score and '-' in score:
			splitScore = score.split('-', 1)
			out.extend([
				('score1', splitScore[0]),
				('score2', splitScore[1])
			])
		out.append(('winner', self.getValue(self.prefix + 'win'), True))
		out.append(('vod', self.getValue(f'vodgame{self.index}'), True))

		return self.generateString([out])
