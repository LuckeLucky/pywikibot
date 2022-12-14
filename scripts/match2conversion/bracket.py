import logging

from scripts.match2conversion.match2exceptions import WikiStyle
log = logging.getLogger(__name__)

from mwparserfromhell.nodes import Template

from .helpers import generate_id
from .match import Match
from .opponent import Opponent, SoloOpponent, TeamOpponent
from scripts.match2conversion.bracket_helper import BracketHelper
from scripts.utils.parser_helper import get_value, sanitize_template

TEAM = 'team'
SOLO = 'solo'

class Bracket(object):
	configs = None
	mappings = None

	def __init__(self, oldTemplateName: str, bracket: Template) -> None:
		self.bracket = sanitize_template(bracket, removeComments = True)	
		self.newName = BracketHelper.get_new_bracket_name(oldTemplateName)
		self.bracketType = TEAM if TEAM in oldTemplateName.lower() else SOLO
		self.shortNames = ''
		self.columnwidth = ''
		self.roundData = {}

	def check_name(self, name:str):
		if ('[' in name) or (']' in name):
			raise WikiStyle

	def get_opponent(self, parameter, scoreKey:str = 'score') -> Opponent:
		if self.bracketType == TEAM:
			teamName = get_value(self.bracket, parameter + 'team')
			teamcsName = get_value(self.bracket, parameter)
			literal = get_value(self.bracket, parameter + 'literal')
			teamScore = get_value(self.bracket, parameter + scoreKey)
			if (teamName is not None):
				self.check_name(teamName)
				return TeamOpponent(teamName, teamScore)
			elif(teamcsName is not None):
				self.check_name(teamcsName)
				return Opponent(teamcsName, teamScore)
			elif(literal is not None):
				return Opponent(literal, teamScore)
			else:
				return None
		elif self.bracketType == SOLO:
			playerName = get_value(self.bracket, parameter)
			playerFlag = get_value(self.bracket, parameter + 'flag')
			playerScore = get_value(self.bracket, parameter + scoreKey)
			if (playerName is None) and (playerScore is None) and (playerFlag is None):
				return None
			return SoloOpponent(playerName, playerScore, '', playerFlag)
		else:
			return None

	def get_summary(self, parameter, index = 0):
		if self.bracket.has(parameter + 'details'):
			templates = self.bracket.get(parameter + 'details').value.filter_templates(recursive = False)
			if len(templates) > index:
				return sanitize_template(templates[index])
		return None

	def get_winner(self, team1Param: str, team2Param) -> int:
		if get_value(self.bracket, team1Param + 'win'):
			return 1
		if get_value(self.bracket, team2Param + 'win'):
			return 2
		return -1

	def populate_round_data(self, match, roundData, lastRound, lowerHeaders):
		id = BracketHelper.get_simplified_id(match['match2id'])
		roundNumber, _, _ = id[1:].partition('M')
		if roundNumber.isnumeric():
			roundNumber = int(roundNumber)
		reset = False
		if id == 'RxMTP':
			round = lastRound
		elif id == 'RxMBR':
			round = lastRound
			round['G'] = round['G'] - 2
			round['W'] = round['W'] - 2
			round['D'] = round['D'] - 2
			reset = True
		else:
			if roundNumber in roundData:
				round = roundData[roundNumber]
			else:
				round = {'R': roundNumber, 'G': 0, 'D': 1, 'W': 1}
		round['G'] = round['G'] + 1

		bd = match['match2bracketdata']

		if 'header' in bd:
			if bd['header'].startswith('!l'):
				lowerHeaders[roundNumber] = round['G']

		opponent1 = None
		winner1Param = ''
		if (not 'toupper' in bd) and not reset:
			param = 'R' + str(round['R']) + 'D' + str(round['D'])
			#RxDx
			opponent1 = self.get_opponent(param)
			winner1Param = param
			round['D'] = round['D'] + 1
		else:
			param = 'R' + str(round['R']) + 'W' + str(round['W'])
			#RxWx
			opponent1 = self.get_opponent(param, scoreKey= 'score2' if reset else 'score')
			winner1Param = param
			round['W'] = round['W'] + 1

		opponent2 = None
		winner2Param = ''
		if (not 'tolower' in bd) and not reset:
			param = 'R' + str(round['R']) + 'D' + str(round['D'])
			#RxDx
			opponent2 = self.get_opponent(param)
			winner2Param = param
			round['D'] = round['D'] + 1
		else:
			param = 'R' + str(round['R']) + 'W' + str(round['W'])
			#RxWx
			opponent2 = self.get_opponent(param, scoreKey= 'score2' if reset else 'score')
			winner2Param = param
			round['W'] = round['W'] + 1

		winner = self.get_winner(winner1Param, winner2Param)
		details = self.get_summary('R' + str(round['R']) + 'G' + str(round['G']), index = 1 if reset else 0)
		match2 = Match(opponent1, opponent2, winner, details, reset)
		self.roundData[id] = match2
		roundData[round['R']] = round
		lastRound = round

		return roundData, lastRound, lowerHeaders

	def handle_custom_mapping(self):
		for roundParam, match1Params in BracketHelper.mapping.items():
			reset = False
			if roundParam == 'RxMBR':
				reset = True
			opp1param = match1Params["opp1"]
			opp2param = match1Params["opp2"]
			details = self.get_summary(match1Params["details"], index = 1 if reset else 0)
			opponent1 = self.get_opponent(opp1param, scoreKey= 'score2' if reset else 'score')
			opponent2 = self.get_opponent(opp2param, scoreKey= 'score2' if reset else 'score')
			winner = self.get_winner(opp1param, opp2param)
			match2 = Match(opponent1, opponent2, winner, details)
			self.roundData[roundParam] = match2

			if "header" in match1Params:
				header = get_value(self.bracket, match1Params["header"])
				if header:
					self.roundData[roundParam + 'header'] = header

	def process(self):
		if (self.bracket is None):
			return

		self.shortNames = get_value(self.bracket, 'shortNames')
		self.columnwidth = get_value(self.bracket, 'column-width')
		if not self.columnwidth:
			self.columnwidth = get_value(self.bracket, 'column-width1')

		roundData = {}
		lowerHeaders = {}
		lastRound = None
		#Mapping via lpdb template data
		for match in BracketHelper.bracketData:
			roundData, lastRound, lowerHeaders = self.populate_round_data(match, roundData, lastRound, lowerHeaders)

		for n in range(1, lastRound['R'] + 1):
			headerUp = get_value(self.bracket, 'R' + str(n))
			if headerUp:
				self.roundData['R' + str(n) + 'M1header'] = headerUp
			headerLow = get_value(self.bracket, 'L' + str(n))
			if headerLow and (n in lowerHeaders):
				self.roundData['R' + str(n) + 'M' + str(lowerHeaders[n]) + 'header'] = headerLow
	
		if BracketHelper.mapping:
			self.handle_custom_mapping()

	def __str__(self) -> str:
		out = '{{Bracket|'+ self.newName + '|id=' + generate_id()
		if self.shortNames:
			out = out + '|forceShortName=true'
		if self.columnwidth:
			out = out + '|matchWidth=' + self.columnwidth
			
		matchOut = ''
		roundOutputOrder = BracketHelper.get_round_output_order()
		for round in roundOutputOrder:
			param = round['matchKey']
			if param + 'header' in self.roundData:
				out = out + '\n|' + param + 'header=' + self.roundData[param + 'header']

			if not param in self.roundData:
				#Todo add empty match
				if param != 'RxMTP' and param != 'RxMBR':
					matchOut = matchOut + '\n|' + param + '=' + '\n'
				continue
			match = self.roundData[param]
			match.process()
			if match.is_valid():
				if param == 'RxMBR':
					#We dont check winner because for reset match final winner == reset winner (match1)
					if (not match.opponent1.score) and (not match.opponent2.score) and (not match.summary):
						continue
				elif param == 'RxMTP':
					if (not match.opponent1.score) and (not match.opponent2.score) and match.winner < 0:
						continue
				header = ''
				if param == 'RxMTP' or param == 'RxMBR':
					if param == 'RxMTP':
						log.info("Third Place Match saved")
						header = '\n\n' + '<!-- Third Place Match -->'
					else:
						log.info("Reset Match saved")
				elif 'header' in round:
					header = BracketHelper.get_header(round['header'])
				matchOut = matchOut + header
				matchOut = matchOut + '\n|' + param + '=' + str(match)

		return out + matchOut + '\n}}'
