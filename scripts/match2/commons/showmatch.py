from mwparserfromhell.nodes import Template
from .opponent import Opponent, TeamOpponent
from .utils import *
from .match import Match

class Showmatch(object):
	Match = Match
	def __init__(self, template: Template) -> None:
		self.template = sanitizeTemplate(template)
		self.data = getTemplateParameters(template)
		self.match = None
		
		self.get_match()

	def get_opponent(self, key: str, scoreKey: str) -> Opponent:
		name = get_value_or_empty(self.data, key)
		score = get_value_or_empty(self.data, scoreKey)
		return TeamOpponent(name, score)
	
	def get_match(self):
		opponent1 = self.get_opponent('team1', 'score1')
		opponent2 = self.get_opponent('team2', 'score2')
		winner = get_value_or_empty(self.data, 'win')
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
