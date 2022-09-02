class Opponent(object):
	
	def __init__(self, name, score):
		self.name = name
		self.score = score

	def __str__(self) -> str:
		out = '{{TeamOpponent|'
		if self.name:
			out = out + self.name
		if self.score:
			out = out + '|score=' + self.score 

		return out + '}}'