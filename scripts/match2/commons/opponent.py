class Opponent(object):	
	def __init__(self, name: str = '', score: str = ''):
		self.name = name
		self.score = score

	def type(self):
		return 'literal'

	def is_bye(self) -> bool:
		return self.name.lower() == 'bye'

	def __str__(self) -> str:
		out = '{{LiteralOpponent|'
		if self.name:
			out = out + self.name
		if self.score:
			out = out + '|score=' + self.score 

		return out + '}}'

class TeamOpponent(Opponent):
	def __init__(self, name: str = '', score: str = ''):
		super().__init__(name, score)

	def type(self):
		return 'team'

	def __str__(self) -> str:
		out = '{{TeamOpponent|'
		if self.name:
			out = out + self.name
		if self.score:
			out = out + '|score=' + self.score 

		return out + '}}'

class SoloOpponent(Opponent):
	def __init__(self, name: str = '', score: str = '', link: str = '', flag: str = '') -> None:
		self.link = link
		self.flag = flag
		super().__init__(name, score)

	def type(self):
		return 'solo'

	def __str__(self) -> str:
		out = '{{SoloOpponent|'
		if self.name:
			out = out + self.name
		if self.link:
			out = out + '|link=' + self.link
		if self.flag:
			out = out + '|flag=' + self.flag
		if self.score:
			out = out + '|score=' + self.score
		return out + '}}'