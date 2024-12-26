from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def __init__(self, index, template) -> None:
		super().__init__(index, template)
		self.prefix = f'g{self.index}'

	def __str__(self) -> str:
		scores = self.getValue(f'{self.prefix}score').split('-')
		if all(score == '' for score in scores):
			scores = ['', '']
		out = [
			self.getFoundPrefix(f'{self.prefix}p1', lambda x: x.replace(self.prefix, '')),
			('p1d', self.getValue(f'p1d{self.index}')),
			self.getFoundPrefix(f'{self.prefix}p2', lambda x: x.replace(self.prefix, '')),
			('p2d', self.getValue(f'p2d{self.index}')),
			[
				('winner', self.getValue(f'{self.prefix}win')),
				('score1', scores[0], True),
				('score2', scores[1], True),
				('vod', self.getValue(f'vodgame{self.index}'), True)
			]
		]

		return self.generateString(out)
