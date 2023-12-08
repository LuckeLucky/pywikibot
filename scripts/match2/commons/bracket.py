from mwparserfromhell.nodes import Template

from .utils import *
from .match import Match
from .opponent import Opponent, SoloOpponent, TeamOpponent
from .bracket_helper import BracketHelper

TEAM = 'team'
SOLO = 'solo'

RESET_MATCH = 'RxMBR'
THIRD_PLACE_MATCH = 'RxMTP'

class Bracket(object):
	new_match = Match
	def __init__(self, oldTemplateName: str, bracket: Template) -> None:
		self.bracket = sanitize_template(bracket, removeComments = True)	
		self.newName = BracketHelper.get_new_bracket_name(oldTemplateName)
		self.bracketType = TEAM if TEAM in oldTemplateName.lower() else SOLO
		self.shortNames = ''
		self.columnwidth = ''
		self.roundData = {}

	def match_class(self):
		return Match

	def get_team_opponent(self, key: str, scoreKey: str) -> Opponent:
		name = get_parameter_str(self.bracket, key + 'team')
		literal = get_parameter_str(self.bracket, key + 'literal')
		score = get_parameter_str(self.bracket, key + scoreKey)
		if name is not None:
			return TeamOpponent(name, score)
		if literal is not None:
			return Opponent(name, score)
		return None

	def get_solo_opponent(self, key: str, scoreKey: str) -> Opponent:
		name = get_parameter_str(self.bracket, key)
		flag = get_parameter_str(self.bracket, key + 'flag')
		score = get_parameter_str(self.bracket, key + scoreKey)
		if (name is None) and (score is None) and (flag is None):
			return None
		return SoloOpponent(name, score, '', flag)

	def get_opponent(self, key: str, scoreKey: str = 'score') -> Opponent:
		if self.bracketType == TEAM:
			return self.get_team_opponent(key, scoreKey)
		elif self.bracketType == SOLO:
			return self.get_solo_opponent(key, scoreKey)

	def get_details(self, key, index = 0):
		if self.bracket.has(key + 'details'):
			templates = self.bracket.get(key + 'details').value.filter_templates(recursive = False)
			if len(templates) > index:
				return sanitize_template(templates[index])
		return None

	def get_winner(self, team1Key: str, team2Key) -> int:
		if get_parameter_str(self.bracket, team1Key + 'win'):
			return '1'
		if get_parameter_str(self.bracket, team2Key + 'win'):
			return '2'
		return ''

	def populate_round_data(self, match, roundData, lastRound, lowerHeaders):
		id = BracketHelper.get_simplified_id(match['match2id'])
		roundNumber, _, _ = id[1:].partition('M')
		if roundNumber.isnumeric():
			roundNumber = int(roundNumber)
		reset = False
		if id == THIRD_PLACE_MATCH:
			round = lastRound
		elif id == RESET_MATCH:
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

		details = self.get_details('R' + str(round['R']) + 'G' + str(round['G']), index = 1 if reset else 0)
		winner = self.get_winner(winner1Param, winner2Param)
		if winner:
			if not details:
				details = Template("FAKE")
			details.add('winner', winner)
		match2 = self.match_class()(opponent1, opponent2, details)
		self.roundData[id] = match2
		roundData[round['R']] = round
		lastRound = round

		return roundData, lastRound, lowerHeaders

	def handle_custom_mapping(self):
		for roundParam, match1Params in BracketHelper.mapping.items():
			reset = False
			if roundParam == RESET_MATCH:
				reset = True
			opp1param = match1Params["opp1"]
			opp2param = match1Params["opp2"]
			details = self.get_details(match1Params["details"], index = 1 if reset else 0)
			opponent1 = self.get_opponent(opp1param, scoreKey= 'score2' if reset else 'score')
			opponent2 = self.get_opponent(opp2param, scoreKey= 'score2' if reset else 'score')
			winner = self.get_winner(opp1param, opp2param)
			if winner:
				if not details:
					details = Template("FAKE")
				details.add('winner', winner)
			match2 = self.match_class()(opponent1, opponent2, details)
			self.roundData[roundParam] = match2

			if "header" in match1Params:
				header = get_parameter_str(self.bracket, match1Params["header"])
				if header:
					self.roundData[roundParam + 'header'] = header

	def process(self):
		if (self.bracket is None):
			return

		self.shortNames = get_parameter_str(self.bracket, 'shortNames')
		self.columnwidth = get_parameter_str(self.bracket, 'column-width')
		if not self.columnwidth:
			self.columnwidth = get_parameter_str(self.bracket, 'column-width1')

		roundData = {}
		lowerHeaders = {}
		lastRound = None
		#Mapping via lpdb template data
		for match in BracketHelper.bracketData:
			roundData, lastRound, lowerHeaders = self.populate_round_data(match, roundData, lastRound, lowerHeaders)

		for n in range(1, lastRound['R'] + 1):
			headerUp = get_parameter_str(self.bracket, 'R' + str(n))
			if headerUp:
				self.roundData['R' + str(n) + 'M1header'] = headerUp
			headerLow = get_parameter_str(self.bracket, 'L' + str(n))
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
				if param != THIRD_PLACE_MATCH and param != RESET_MATCH:
					matchOut = matchOut + '\n|' + param + '=' + '\n'
				continue
			match = self.roundData[param]
			if match.is_valid():
				if param == RESET_MATCH:
					#We dont check winner because for reset match final winner == reset winner (match1)
					if (not match.opponent1.score) and (not match.opponent2.score) and (not match.template or match.template.name == "FAKE"):
						continue
				elif param == THIRD_PLACE_MATCH:
					if (not match.opponent1.score) and (not match.opponent2.score) and match.winner < 0:
						continue
				header = ''
				if param == THIRD_PLACE_MATCH or param == RESET_MATCH:
					if param == THIRD_PLACE_MATCH:
						header = '\n\n' + '<!-- Third Place Match -->'
				elif 'header' in round:
					header = BracketHelper.get_header(round['header'])
				matchOut = matchOut + header
				matchOut = matchOut + '\n|' + param + '=' + str(match)

		return out + matchOut + '\n}}'