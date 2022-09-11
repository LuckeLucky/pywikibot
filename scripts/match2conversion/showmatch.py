from mwparserfromhell.nodes import Template

from scripts.match2conversion.opponent import Opponent
from scripts.utils.parser_helper import get_value, sanitize_template

from .match import Match
from .helpers import generate_id

class Showmatch(object):
	
	def __init__(self, showmatch: Template) -> None:
		self.showmatchTemplate = sanitize_template(showmatch)

		self.match = None

	def get_opponent(self, opponentIndex: int) -> Opponent:
		teamName = get_value(self.showmatchTemplate, 'team' + str(opponentIndex))
		teamScore = get_value(self.showmatchTemplate, 'score' + str(opponentIndex))
		return Opponent(teamName, teamScore)

	def get_summary(self):
		if self.showmatchTemplate.has('details'):
			return sanitize_template(self.showmatchTemplate.get('details').value.filter_templates()[0])
		return None

	def get_winner(self) -> int:
		winner = get_value(self.showmatchTemplate, 'win')
		if winner in ['1', '2', '0']:
			return int(winner)
		elif winner == 'draw':
			return 0
		else:
			return -1

	def process(self):
		opponent1 = self.get_opponent(1)
		opponent2 = self.get_opponent(2)
		details = self.get_summary()
		winner = self.get_winner()

		self.match = Match(opponent1, opponent2, winner, details)
		self.match.process()

	def __str__(self) -> str:
		out = '{{SingleMatch|id=' + generate_id()

		if self.match:
			out = out + '\n|' + str(self.match)

		return out + '\n}}'