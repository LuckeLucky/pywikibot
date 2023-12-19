from mwparserfromhell.nodes import Template
from .opponent import Opponent, TeamOpponent
from .utils import sanitizeTemplate, getTemplateParameters, getValueOrEmpty, getNestedTemplateFromTemplate, generateId
from .match import Match

class Showmatch(object):
	Match = Match
	def __init__(self, template: Template) -> None:
		self.template = sanitizeTemplate(template)
		self.data = getTemplateParameters(template)
		self.match = None
		self.getMatch()

	def getOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = getValueOrEmpty(self.data, key)
		score = getValueOrEmpty(self.data, scoreKey)
		return TeamOpponent(name, score)

	def getMatch(self):
		opponent1 = self.getOpponent('team1', 'score1')
		opponent2 = self.getOpponent('team2', 'score2')
		winner = getValueOrEmpty(self.data, 'win')
		details = getNestedTemplateFromTemplate(self.template, 'details')
		if winner:
			if not details:
				details = Template("FAKE")
			details.add('winner', winner)
		self.match = self.Match([opponent1, opponent2], details)

	def __str__(self) -> str:
		out = '{{SingleMatch|id=' + generateId()

		if self.match:
			out = out + '\n|' + str(self.match)

		return out + '\n}}'
