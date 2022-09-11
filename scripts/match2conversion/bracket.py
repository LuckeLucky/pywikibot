import json
from functools import cmp_to_key
from os import name
from mwparserfromhell.nodes import Template

from .helpers import generate_id
from .match import Match
from .opponent import Opponent
from .bracket_alias import bracketAlias
from scripts.utils.parser_helper import get_value, sanitize_template

from pathlib import Path

class Bracket(object):
	configs = None
	mappings = None

	@staticmethod
	def check_support(templateName: str):
		return templateName in bracketAlias

	@staticmethod
	def read_config():
		p = Path(__file__).with_name('bracket_templates.json')
		file = p.open()
		data = json.load(file)
		Bracket.configs = data

	@staticmethod
	def read_custom_mappings():
		p = Path(__file__).with_name('custom_mappings.json')
		file = p.open()
		data = json.load(file)
		Bracket.mappings = data

	@staticmethod
	def get_simplified_id(id: str):
		id = id.split('_')[1] if len(id.split('_')) > 1 else id
		if id == 'RxMTP':
			return id
		elif id == 'RxMBR':
			return id
		else:
			id = id.replace('-', '')
			roundNumber, _, matchNumber = id[1:].partition('M')
			return 'R' + str(int(roundNumber)) + 'M' + str(int(matchNumber))

	def __init__(self, oldTemplateName: str, bracket: Template) -> None:
		if Bracket.configs is None:
			Bracket.read_config()
		if Bracket.mappings is None:
			Bracket.read_custom_mappings()
		self.oldTemplateName = oldTemplateName
		self.newTemplateName = 'Bracket/' + bracketAlias[self.oldTemplateName]
		self.bracket = sanitize_template(bracket, removeComments = True)

		self.lpdbMatches = Bracket.configs[self.newTemplateName]
		self.customMapping = Bracket.mappings[self.newTemplateName] if self.newTemplateName in Bracket.mappings else None
		self.roundData = {}

		self.shortNames = ''
		self.columnwidth = ''

	def get_opponent(self, parameter, scoreKey:str = 'score') -> Opponent:
		teamName = get_value(self.bracket, parameter + 'team')
		teamScore = get_value(self.bracket, parameter + scoreKey)
		if (teamName is None) and (teamScore is None):
			return None
		return Opponent(teamName, teamScore)

	def get_summary(self, parameter, index = 0):
		if self.bracket.has(parameter + 'details'):
			templates = self.bracket.get(parameter + 'details').value.filter_templates()
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
		id = Bracket.get_simplified_id(match['match2id'])
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
		match2 = Match(opponent1, opponent2, winner, details)
		self.roundData[id] = match2
		roundData[round['R']] = round
		lastRound = round

		return roundData, lastRound, lowerHeaders

	def handle_custom_mapping(self):
		for roundParam, match1Param in self.customMapping.items():
			details = self.get_summary(match1Param["details"])
			opp1param = match1Param["opp1"]
			opp2param = match1Param["opp2"]
			opponent1 = self.get_opponent(opp1param)
			opponent2 = self.get_opponent(opp2param)
			winner = self.get_winner(opp1param, opp2param)
			match2 = Match(opponent1, opponent2, winner, details)
			self.roundData[roundParam] = match2

	def get_round_output_order(self):
		#Return the expected round output order
		_bracketDataList = []

		for match in self.lpdbMatches:
			id = Bracket.get_simplified_id(match['match2id'])
			bracketData = match['match2bracketdata']
			bracketData['matchKey'] = id
			_bracketDataList.append(bracketData)

		def sortKey(bracketData):
			coordinates = bracketData['coordinates'] if 'coordinates' in bracketData else None
			if bracketData['matchKey'] == 'RxMTP' or bracketData['matchKey'] == 'RxMBR':
				#RxMTP and RxMBR entries appear immediately after the match they're attached to
				#So that match need to be found
				finalBracketData = next((x for x in _bracketDataList if (('thirdplace' in x) or ('bracketreset' in x))), None)
				result = sortKey(finalBracketData)
				result.append(1)
				return result
			elif coordinates['semanticDepth'] == 0:
				return [1, -coordinates['sectionIndex']]
			else:
				return [0, coordinates['sectionIndex'], coordinates['roundIndex'], coordinates['matchIndexInRound']]

		def compare(itemA, itemB):
			iteamAsort = sortKey(itemA)
			iteamBsort = sortKey(itemB)

			for index, _ in enumerate(min(iteamAsort, iteamBsort)):
				if iteamAsort[index] < iteamBsort[index]:
					return -1
				elif iteamAsort[index] > iteamBsort[index]:
					return 1
			
			return 1 if len(itemA) < len(itemB) else -1

		_bracketDataList = sorted(_bracketDataList, key = cmp_to_key(compare))

		return [x['matchKey'] for x in _bracketDataList]

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
		for match in self.lpdbMatches:
			roundData, lastRound, lowerHeaders = self.populate_round_data(match, roundData, lastRound, lowerHeaders)

		for n in range(1, lastRound['R'] + 1):
			headerUp = get_value(self.bracket, 'R' + str(n))
			if headerUp:
				self.roundData['R' + str(n) + 'M1header'] = headerUp
			headerLow = get_value(self.bracket, 'L' + str(n))
			if headerLow and (n in lowerHeaders):
				self.roundData['R' + str(n) + 'M' + str(lowerHeaders[n]) + 'header'] = headerLow
	
		if self.customMapping:
			self.handle_custom_mapping()

	def __str__(self) -> str:
		out = '{{Bracket|'+ self.newTemplateName + '|id=' + generate_id()
		if self.shortNames:
			out = out + '|forceShortName=true'
		if self.columnwidth:
			out = out + '|matchWidth=' + self.columnwidth
		out = out + '\n'
			
		matchOut = ''
		roundOutputOrder = self.get_round_output_order()
		for param in roundOutputOrder:
			if param + 'header' in self.roundData:
				out = out + '|' + param + 'header=' + self.roundData[param + 'header'] + '\n'
			if not param in self.roundData:
				continue
			match = self.roundData[param]
			match.process()
			if match.isValid():
				matchOut = matchOut + '|' + param + '=' + str(match) + '\n'

		return out + matchOut + '}}'