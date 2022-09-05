from cgitb import reset
import json
from mwparserfromhell.nodes import Template

from .helpers import generate_id
from .match import Match
from .opponent import Opponent
from .bracket_alias import bracketAlias
from scripts.utils.parser_helper import get_value, sanitize_template

from pathlib import Path

class Bracket(object):
	configs = None

	@staticmethod
	def check_support(templateName: str):
		return templateName in bracketAlias

	@staticmethod
	def read_config():
		p = Path(__file__).with_name('bracket_templates.json')
		file = p.open()
		data = json.load(file)
		Bracket.configs = data

	def __init__(self, oldTemplateName: str, bracket: Template) -> None:
		if Bracket.configs is None:
			Bracket.read_config()
		self.oldTemplateName = oldTemplateName
		self.bracket = sanitize_template(bracket)

		self.roundData = {}
		self.bracketData = {}
		self.lastRound = None

	def get_opponent(self, parameter) -> Opponent:
		teamName = get_value(self.bracket, parameter + 'team')
		teamScore = get_value(self.bracket, parameter + 'score')
		return Opponent(teamName, teamScore)

	def get_summary(self, parameter):
		if self.bracket.has(parameter + 'details'):
			return sanitize_template(self.bracket.get(parameter + 'details').value.filter_templates()[0])
		return None

	def get_winner(self, parameter) -> int:
		if get_value(self.bracket, parameter + 'win'):
			return 1
		return 0

	def get_match_mappings(self, match):
		id = match['match2id'].split('_')[1] or match['match2id']
		id = id.replace('-', '')
		
		reset = False
		if id == 'RxMTP':
			round = self.lastRound
		elif id == 'RxMBR':
			round = self.lastRound
			round.G = round.G - 2
			round['W'] = round['W'] - 2
			round['D'] = round['D'] - 2
			reset = True
		else:
			id = id[1:]
			roundNumber = int(id.split('M')[0])
			if roundNumber in self.roundData:
				round = self.roundData[roundNumber]
			else:
				round = {'R': roundNumber, 'G': 0, 'D': 1, 'W': 1}
		round['G'] = round['G'] + 1

		bd = match['match2bracketdata']

		opponent1 = None
		winner1 = 0
		if (not 'toupper' in bd) and not reset:
			param = 'R' + str(round['R']) + 'D' + str(round['D'])
			#RxDx
			opponent1 = self.get_opponent(param)
			winner1 = self.get_winner(param)
			round['D'] = round['D'] + 1
		else:
			param = 'R' + str(round['R']) + 'W' + str(round['W'])
			#RxWx
			opponent1 = self.get_opponent(param)
			winner1 = self.get_winner(param)
			round['W'] = round['W'] + 1

		opponent2 = None
		winner2 = 0
		if (not 'tolower' in bd) and not reset:
			param = 'R' + str(round['R']) + 'D' + str(round['D'])
			#RxDx
			opponent2 = self.get_opponent(param)
			winner2 = self.get_winner(param)
			round['D'] = round['D'] + 1
		else:
			param = 'R' + str(round['R']) + 'W' + str(round['W'])
			#RxWx
			opponent2 = self.get_opponent(param)
			winner2 = self.get_winner(param)
			round['W'] = round['W'] + 1

		details = self.get_summary('R' + str(round['R']) + 'G' + str(round['G']))
		winner = winner1 > winner2 and 1 or 0
		self.bracketData[id] = Match(opponent1, opponent2, winner, details)
		self.lastRound = round
		self.roundData[round['R']] = round

	def process(self):
		if (self.bracket is None):
			return

		templateID = 'Bracket/' + bracketAlias[self.oldTemplateName]
		matches = Bracket.configs[templateID]

		for match in matches:
			self.get_match_mappings(match)

	def get_header(self, parameter):
		return get_value(self.bracket, parameter)

	def __str__(self) -> str:
		return ''