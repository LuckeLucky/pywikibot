from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def __str__(self):
		prefix = self.prefix
		out = [
			('map', self.getValue(prefix)),
			self.getFoundPrefix(prefix + 't1c', lambda key: key.replace(prefix, '')),
			self.getFoundPrefix(prefix + 't2c', lambda key: key.replace(prefix, '')),
			[
				('winner', self.getValue(prefix + 'win')),
				('score1', self.getValue(prefix + 't1score')),
				('score2', self.getValue(prefix + 't2score')),
			],
			('vod', self.getValue(f'vodgame{self.index}'), True)
		]

		return self.generateString(out)
