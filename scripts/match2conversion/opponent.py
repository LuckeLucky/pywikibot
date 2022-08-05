class Opponent(object):
	
	def __init__(self, name, score):
		self._name = name
		self._score = score

	def __str__(self) -> str:
		out = '{{TeamOpponent|'
		if self._name != '':
			out = out + self._name
		if self._score != '':
			out = out + '|score=' + self._score 

		return out + '}}'