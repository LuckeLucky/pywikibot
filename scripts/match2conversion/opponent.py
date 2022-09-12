class Opponent(object):
	
	def __init__(self, name: str = '', score: str = ''):
		self.name = name
		self.score = score

	def is_bye(self) -> bool:
		return self.name.lower() == 'bye'

	def __str__(self) -> str:
		out = '{{TeamOpponent|'
		if self.name:
			out = out + self.name
		if self.score:
			out = out + '|score=' + self.score 

		return out + '}}'