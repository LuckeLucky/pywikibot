from .template import Template
from .templateutils import TemplateUtils
from .opponent import Opponent, TeamOpponent, SoloOpponent
from .match import Match as commonsMatch
from .utils import importClass

class Singlematch(TemplateUtils):
	language: str = None
	matchClass: commonsMatch = None

	def __init__(self, template: Template) -> None:
		if self.matchClass is None:
			self.matchClass = importClass(self.language, 'Match')

		super().__init__(template)
		self.id: str = self.getValue('id')
		self.bracketType: str = self.getValue('type')
		self.match: commonsMatch = None
		self.getMatch()

	def getTeamOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.getValue(key)
		score = self.getValue(scoreKey)
		return TeamOpponent(name = name, score = score)

	def getSoloOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.getValue(key)
		score = self.getValue(scoreKey)
		return SoloOpponent(name = name, score = score)

	def getOpponent(self, key: str, scoreKey: str) -> Opponent:
		opponentGet = getattr(self, 'get' + str(self.bracketType).capitalize() + 'Opponent')
		if not opponentGet:
			raise ValueError(self.bracketType + 'is not supported')
		return opponentGet(key, scoreKey)

	def getMatch(self):
		opponent1 = self.getOpponent('team1', 'score1')
		opponent2 = self.getOpponent('team2', 'score2')
		winner = self.getValue('win')
		details = self.template.getNestedTemplate('details')
		if winner:
			if not details:
				details = Template.createFakeTemplate()
			details.add('winner', winner)
		self.match = self.matchClass([opponent1, opponent2], Template(details))

	def __str__(self) -> str:
		out = '{{SingleMatch|id=' + self.id

		if self.match:
			out = out + '\n|' + str(self.match)

		return out + '\n}}'
