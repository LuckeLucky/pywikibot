import json
from functools import cmp_to_key
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

	@staticmethod
	def simplify_id(id: str):
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
		self.oldTemplateName = oldTemplateName
		self.newTemplateName = 'Bracket/' + bracketAlias[self.oldTemplateName]
		self.bracket = sanitize_template(bracket, removeComments = True)

		self.lpdbMatches = Bracket.configs[self.newTemplateName]
		
		self.idToMatch = {}
		self.idToHeader = {}

		self.shortNames = ''
		self.columnwidth = ''

	def get_opponent(self, parameter) -> Opponent:
		teamName = get_value(self.bracket, parameter + 'team')
		teamScore = get_value(self.bracket, parameter + 'score')
		if (teamName is None) and (teamScore is None):
			return None
		return Opponent(teamName, teamScore)

	def get_summary(self, parameter):
		if self.bracket.has(parameter + 'details'):
			return sanitize_template(self.bracket.get(parameter + 'details').value.filter_templates()[0])
		return None

	def get_winner(self, team1Param: str, team2Param) -> int:
		if get_value(self.bracket, team1Param + 'win'):
			return 1
		if get_value(self.bracket, team2Param + 'win'):
			return 2
		return -1

	def handle_round_mapping(self, match, roundData, lastRound):
		id = Bracket.simplify_id(match['match2id'])
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
		
		header = get_value(self.bracket, 'R' + str(roundNumber))
		if header:
			self.idToHeader['R' + str(roundNumber) + 'M1header'] = header
		if ('header' in bd) and (bd['header'].startswith('!l')):
			lowerHeader = get_value(self.bracket, 'L' + str(round['G']))
			if lowerHeader:
				self.idToHeader['R' + str(roundNumber) + 'M' + str(round['G']) + 'header'] = lowerHeader

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
			opponent1 = self.get_opponent(param)
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
			opponent2 = self.get_opponent(param)
			winner2Param = param
			round['W'] = round['W'] + 1

		winner = self.get_winner(winner1Param, winner2Param)
		details = self.get_summary('R' + str(round['R']) + 'G' + str(round['G']))
		match2 = Match(opponent1, opponent2, winner, details)
		if match2.isValid():
			self.idToMatch[id] = match2
			roundData[round['R']] = round
			lastRound = round

		return roundData, lastRound

	def get_round_output_order(self):
		#Return the expected round output order
		_bracketDataList = []

		for match in self.lpdbMatches:
			id = Bracket.simplify_id(match['match2id'])
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

		def compare(iteamA, itemB):
			iteamAsort = sortKey(iteamA)
			iteamBsort = sortKey(itemB)

			for index, _ in enumerate(min(iteamAsort, iteamBsort)):
				if iteamAsort[index] < iteamBsort[index]:
					return -1
				elif iteamAsort[index] > iteamBsort[index]:
					return 1
			
			return 1 if len(iteamA) < len(itemB) else -1

		_bracketDataList = sorted(_bracketDataList, key=cmp_to_key(compare))

		return [x['matchKey'] for x in _bracketDataList]

	def order_header_keys(self):
		pass


	def process(self):
		if (self.bracket is None):
			return

		roundData = {}
		lastRound = None
		for match in self.lpdbMatches:
			roundData, lastRound = self.handle_round_mapping(match, roundData, lastRound)

		self.shortNames = get_value(self.bracket, 'shortNames')
		self.columnwidth = get_value(self.bracket, 'column-width')
		if not self.columnwidth:
			self.columnwidth = get_value(self.bracket, 'column-width1')

	def __str__(self) -> str:
		out = '{{Bracket|'+ self.newTemplateName + '|id=' + generate_id()
		if self.shortNames:
			out = out + '|forceShortName=true'
		if self.columnwidth:
			out = out + '|matchWidth=' + self.columnwidth
		out = out + '\n'

		roundOutputOrder = self.get_round_output_order()
		for param in roundOutputOrder:
			if not param in self.idToMatch:
				continue
			match = self.idToMatch[param]
			match.process()
			out = out + '|' + param + '=' + str(match) + '\n'

		return out + '}}'