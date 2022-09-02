from mwparserfromhell.nodes import Template
from .helpers import generate_id
from .match import Match
from .opponent import Opponent
from ..utils import sanitize_template

from pathlib import Path

SUPPORTED_TEMPLATES = [
	'32DETeamBracket',
	'2SETeamBracket',
	'8SE2STeamBracket'
]

class Bracket(object):

	def __init__(self, oldTemplateName: str, bracket: Template) -> None:
		self.oldTemplateName = oldTemplateName
		self.bracket = sanitize_template(bracket)

	@staticmethod
	def check_support(templateName: str):
		return templateName in SUPPORTED_TEMPLATES

	def get_opponent(self, parameter):
		if self.bracket.has(parameter + 'team'):
			teamName = str(self.bracket.get(parameter + 'team').value)
			teamScore = ''
			if self.bracket.has(parameter + 'score'):
				teamScore = str(self.bracket.get(parameter + 'score').value)
		
			return Opponent(teamName, teamScore)
		return None

	def get_summary(self, parameter):
		if self.bracket.has(parameter + 'details'):
			return sanitize_template(self.bracket.get(parameter + 'details').value.filter_templates()[0])
		return None

	def get_winner(self, team1parameter, team2parameter) -> int:
		if self.bracket.has(team1parameter + 'win'):
			if str(self.bracket.get(team1parameter + 'win').value):
				return 1
		if self.bracket.has(team2parameter + 'win'):
			if str(self.bracket.get(team2parameter + 'win').value):
				return 2
		return 0

	def __str__(self) -> str:
		p = Path(__file__).with_name('bracketconfigs')
		p = p / (self.oldTemplateName + '.txt')
		file = p.open('r')

		wikicode = []
		resetMatch = False
		hasResetMatch = False
		for line in file:
			if 'id=' in line:
				wikicode.append(line.replace('id=', 'id=' + generate_id()))
			elif line.startswith('|R') and (not 'header' in line):
				match2parameter, equal, matchParameters = line.partition('=')
				matchParameters =  matchParameters.rstrip()
				if matchParameters:
					parameters = matchParameters.split('*')

					opponent1 = self.get_opponent(parameters[0])
					opponent2 = self.get_opponent(parameters[1])
					details = self.get_summary(parameters[2])
					winner = self.get_winner(parameters[0], parameters[1])
					if match2parameter == '|RxMTP':
						hasResetMatch = True
						if opponent1 and opponent2 and details:
							resetMatch = True
					match = Match(opponent1, opponent2, winner)
					match.set_summary(details)
					match.process()
					wikicode.append(match2parameter + equal + str(match) + '\n')
			else:
				wikicode.append(line)

		if hasResetMatch:
			#Remove third place things
			if not resetMatch:
				for _ in range(3):
					wikicode.pop(len(wikicode) - 2)
		return ''.join(wikicode)