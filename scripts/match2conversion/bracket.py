from mwparserfromhell.nodes import Template
from .helpers import generate_id
from .match import Match
from .opponent import Opponent
from ..utils import sanitize_template

from pathlib import Path

class Bracket(object):

	def __init__(self, oldTemplateName: str, bracket: Template) -> None:
		self.oldTemplate = oldTemplateName
		self.bracket = sanitize_template(bracket)

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

	def __str__(self) -> str:
		p = Path(__file__).with_name('bracketconfigs')
		p = p / (self.oldTemplate + '.txt')
		file = p.open('r')

		newBracket = ''
		for line in file:
			if 'id=' in line:
				line = line.replace('id=', 'id=' + generate_id())
			if line.startswith('|R') and (not 'header' in line):
				match2parameter, equal, matchParameters = line.partition('=')
				matchParameters =  matchParameters.rstrip()
				if matchParameters:
					parameters = matchParameters.split('*')

					opponent1 = self.get_opponent(parameters[0])
					opponent2 = self.get_opponent(parameters[1])
					details = self.get_summary(parameters[2])
					match = Match(opponent1, opponent2)
					match.set_summary(details)
					match.process()

					newBracket = newBracket + match2parameter + equal + str(match) + '\n'
			else:
				newBracket = newBracket + line


		return newBracket