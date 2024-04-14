class Opponent:
	def __init__(self, opponentType = 'literal', **kwargs):
		self.kwargs = kwargs
		self.opponentType: str = opponentType

	def __str__(self) -> str:
		out = '{{' + self.opponentType.capitalize() + 'Opponent|'

		name = self.kwargs.pop('name', '')
		if name:
			out += name
		for key, value in self.kwargs.items():
			if value:
				out += f'|{key}={value}'

		return out + '}}'

class TeamOpponent(Opponent):
	def __init__(self, opponentType='team', **kwargs):
		super().__init__(opponentType, **kwargs)

class SoloOpponent(Opponent):
	def __init__(self, opponentType='solo', **kwargs):
		super().__init__(opponentType, **kwargs)
