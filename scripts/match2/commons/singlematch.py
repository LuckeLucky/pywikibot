from .template import Template
from .opponent import Opponent, TeamOpponent
from .match import Match as commonsMatch
from .utils import generateId, importClass

class Singlematch:
	language: str = None
	matchClass: commonsMatch = None

	def __init__(self, template: Template) -> None:
		if self.matchClass is None:
			self.matchClass = importClass(self.language, 'Match')
		
		self.template: Template = template
		self.id: str = self.template.getValue('id')
		if not self.id:
			self.id = generateId()
		self.match: commonsMatch = None
		self.getMatch()

	def getOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.template.getValue(key)
		score = self.template.getValue(scoreKey)
		return TeamOpponent(name, score)

	def getMatch(self):
		opponent1 = self.getOpponent('team1', 'score1')
		opponent2 = self.getOpponent('team2', 'score2')
		winner = self.template.getValue('win')
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
