from mwparserfromhell.nodes import Template
from .opponent import Opponent, TeamOpponent
from .utils import sanitizeTemplate, getStringFromTemplate, getValueOrEmpty, getNestedTemplateFromTemplate
from .match import Match

class Showmatch:
	Match = Match
	def __init__(self, template: Template) -> None:
		self.template: Template = sanitizeTemplate(template)
		self.id: str = getStringFromTemplate(self.template, 'id')
		self.match: Match = None
		self.getMatch()

	def getOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = getStringFromTemplate(self.template, key)
		score = getStringFromTemplate(self.template, scoreKey)
		return TeamOpponent(name, score)

	def getMatch(self):
		opponent1 = self.getOpponent('team1', 'score1')
		opponent2 = self.getOpponent('team2', 'score2')
		winner = getValueOrEmpty(self.template, 'win')
		details = getNestedTemplateFromTemplate(self.template, 'details')
		if winner:
			if not details:
				details = Template("FAKE")
			details.add('winner', winner)
		self.match = self.Match([opponent1, opponent2], details)

	def __str__(self) -> str:
		out = '{{SingleMatch|id=' + self.id

		if self.match:
			out = out + '\n|' + str(self.match)

		return out + '\n}}'
