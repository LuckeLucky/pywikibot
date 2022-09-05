from mwparserfromhell.nodes import Template

from .helpers import generate_id
from .match import Match
from .opponent import Opponent
from scripts.utils.parser_helper import get_value, sanitize_template

from pathlib import Path

SUPPORTED_TEMPLATES = [
	'32DETeamBracket',
	'2SETeamBracket',
	'8SE2STeamBracket'
]

class Bracket(object):

	def __init__(self, oldTemplateName: str, bracket: Template) -> None:
		self.oldTemplateName = oldTemplateName
		self.bracket = sanitize_template(bracket, removeComments=True)

	@staticmethod
	def check_support(templateName: str):
		return templateName in SUPPORTED_TEMPLATES

	def get_opponent(self, parameter) -> Opponent:
		teamName = get_value(self.bracket, parameter + 'team')
		teamScore = get_value(self.bracket, parameter + 'score')
		return Opponent(teamName, teamScore)

	def get_summary(self, parameter):
		if self.bracket.has(parameter + 'details'):
			return sanitize_template(self.bracket.get(parameter + 'details').value.filter_templates()[0])
		return None

	def get_winner(self, team1parameter, team2parameter) -> int:
		if get_value(self.bracket, team1parameter + 'win'):
			return 1
		if get_value(self.bracket, team2parameter + 'win'):
			return 2
		return 0

	def get_header(self, parameter):
		return get_value(self.bracket, parameter)

	def handle_round(self, wikicode: list, line: str):
		match2parameter, equal, matchParameters = line.partition('=')
		matchParameters = matchParameters.rstrip()
		#Means we don't have a mapping
		if not matchParameters:
			return

		if 'header' in match2parameter:
			header = self.get_header(matchParameters)
			if header:
				wikicode.append(match2parameter + equal + header + '\n')
		else:
			parameters = matchParameters.split('*')
			opponent1 = self.get_opponent(parameters[0])
			opponent2 = self.get_opponent(parameters[1])
			details = self.get_summary(parameters[2])
			winner = self.get_winner(parameters[0], parameters[1])

			match = Match(opponent1, opponent2, winner, details)
			match.process()

			if '|RxMTP' in match2parameter:
				#Means all match mapping to reset match are empty
				if ((not get_value(parameters[0]))
					and (not get_value(parameters[1]))
					and (not get_value(parameters[2]))):
					#Pop <!-- Third Place Match --> and newline
					wikicode.pop(len(wikicode) - 1)
					wikicode.pop(len(wikicode) - 2)
					return

			wikicode.append(match2parameter + equal + str(match) + '\n')

	def __str__(self) -> str:
		p = Path(__file__).with_name('bracketconfigs')
		p = p / (self.oldTemplateName + '.txt')
		file = p.open('r')

		wikicode = []
		for line in file:
			if 'id=' in line:
				wikicode.append(line.replace('id=', 'id=' + generate_id()))
			elif line.startswith('|R'):
				self.handle_round(wikicode, line)	
			else:
				wikicode.append(line)
		
		return ''.join(wikicode)