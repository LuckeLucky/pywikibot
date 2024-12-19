from .template import Template
from .matchgroup import MatchGroup
from .match import Match as commonsMatch
from .utils import importClass

class Singlematch(MatchGroup):
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

	def getMatch(self) -> None:
		opponent1 = self.getOpponent(self.template, 'team1', 'score1')
		opponent2 = self.getOpponent(self.template, 'team2', 'score2')
		winner = self.getValue('win')
		details = self.template.getNestedTemplate('details')
		if winner:
			if not details:
				details = Template.createFakeTemplate()
			details.add('winner', winner)
		self.match = self.matchClass([opponent1, opponent2], Template.initFromTemplate(details))

	def __str__(self) -> str:
		out = '{{SingleMatch|id=' + self.id

		if self.match:
			out = out + '\n|' + str(self.match)

		return out + '\n}}'
