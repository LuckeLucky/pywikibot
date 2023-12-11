from mwparserfromhell.nodes import Template
import copy
import json

from functools import cmp_to_key
from pathlib import Path

from .utils import *
from .match import Match
from .opponent import Opponent, SoloOpponent, TeamOpponent

TEAM = 'team'
SOLO = 'solo'

RESET_MATCH = 'RxMBR'
THIRD_PLACE_MATCH = 'RxMTP'

class Bracket(object):
	bracketAlias: dict = {
		'2SETeamBracket': '2',
		'2SEBracket': '2',
		'4SETeamBracket': '4',
		'4SEBracket': '4',
		'8SETeamBracket': '8',
		'8SEBracket': '8',
		'16SETeamBracket': '16',
		'16SEBracket': '16',
		'32SETeamBracket': '32',
		'32SEBracket': '32',
		'64SETeamBracket': '64',
		'64SEBracket': '64',
		'128SETeamBracket': '128',
		'128SEBracket': '128',
	}
	newTemplateId: str = ""
	bracketData: list = None
	headersData: dict = None
	customMapping: dict = None
	outputOrder: list = None

	@classmethod
	def isSupported(cls, oldTemplateId: str) -> bool:
		"""
			Checks if the old template can be converted
		"""
		return oldTemplateId in cls.bracketAlias
	
	@classmethod
	def getNewTemplateId(cls, oldTemplateId: str) -> str:
		"""
			Returns the new Bracket name
		"""
		return 'Bracket/' + cls.bracketAlias[oldTemplateId]
	
	@classmethod
	def loadBracketData(cls):
		p = Path(__file__).with_name('bracket_templates.json')
		file = p.open()
		data = json.load(file)
		cls.bracketData = data[cls.newTemplateId] if cls.newTemplateId in data else None

	@classmethod
	def loadHeadersData(cls):
		p = Path(__file__).with_name('headers_data.json')
		file = p.open()
		data = json.load(file)
		cls.headersData = data
	
	@classmethod
	def loadCustomMapping(cls):
		pass

	@classmethod
	def load(cls, oldTemplateId: str) -> bool:
		"""
			Load bracket data and custom mappings into memory
			returns true if sucessfull
		"""
		if not cls.isSupported(oldTemplateId):
			return False
		cls.newTemplateId = cls.getNewTemplateId(oldTemplateId)
		cls.loadBracketData()
		cls.loadCustomMapping()
		cls.loadHeadersData()
		return True

	@classmethod
	def getSimplifiedId(cls, id: str) -> str:

		"""
			Simplify round id
			ex. id = 'R01M001' return 'R1M1'
		"""
		id = id.split('_')[1] if len(id.split('_')) > 1 else id
		if id == 'RxMTP':
			return id
		elif id == 'RxMBR':
			return id
		else:
			id = id.replace('-', '')
			roundNumber, _, matchNumber = id[1:].partition('M')
			return 'R' + str(int(roundNumber)) + 'M' + str(int(matchNumber))

	@classmethod
	def getHeader(cls, headerCode: str) -> str:
		if not headerCode:
			return ''

		if headerCode in cls.headersData:
			return '\n\n' + '<!-- ' + cls.headersData[headerCode] + ' -->'
		
		return ''
	
	@classmethod
	def getRoundOutputOrder(cls):
		if cls.outputOrder:
			return cls.outputOrder
		bracketDataList = []

		for match in cls.bracketData:
			id = cls.getSimplifiedId(match['match2id'])
			bracketData = match['match2bracketdata']
			bracketData['matchKey'] = id
			bracketDataList.append(bracketData)

		def sortKey(bracketData):
			if bracketData is None:
				return [0]
			coordinates = bracketData['coordinates'] if 'coordinates' in bracketData else None
			if bracketData['matchKey'] == 'RxMTP' or bracketData['matchKey'] == 'RxMBR':
				#RxMTP and RxMBR entries appear immediately after the match they're attached to
				#So that match need to be found
				finalBracketData = next((x for x in bracketDataList if (('thirdplace' in x) or ('bracketreset' in x))), None)
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

		bracketDataList = sorted(bracketDataList, key = cmp_to_key(compare))
		cls.outputOrder = copy.copy(bracketDataList)

		return bracketDataList

	def __init__(self, oldTemplateId: str, template: Template) -> None:
		self.template = sanitize_template(template, removeComments = True)	
		self.type = TEAM if TEAM in oldTemplateId.lower() else SOLO
		self.shortNames = ''
		self.columnwidth = ''
		self.roundData = {}

	def matchClass(self):
		return Match

	def getTeamOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = get_parameter_str(self.template, key + 'team')
		literal = get_parameter_str(self.template, key + 'literal')
		score = get_parameter_str(self.template, key + scoreKey)
		if name is not None:
			return TeamOpponent(name, score)
		if literal is not None:
			return Opponent(name, score)
		return None

	def getSoloOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = get_parameter_str(self.template, key)
		flag = get_parameter_str(self.template, key + 'flag')
		score = get_parameter_str(self.template, key + scoreKey)
		if (name is None) and (score is None) and (flag is None):
			return None
		return SoloOpponent(name, score, '', flag)

	def getOpponent(self, key: str, scoreKey: str = 'score') -> Opponent:
		if self.type == TEAM:
			return self.getTeamOpponent(key, scoreKey)
		elif self.type == SOLO:
			return self.getSoloOpponent(key, scoreKey)

	def getDetails(self, key, index = 0):
		if self.template.has(key + 'details'):
			templates = self.template.get(key + 'details').value.filter_templates(recursive = False)
			if len(templates) > index:
				return sanitize_template(templates[index])
		return None

	def getWinner(self, team1Key: str, team2Key) -> int:
		if get_parameter_str(self.template, team1Key + 'win'):
			return '1'
		if get_parameter_str(self.template, team2Key + 'win'):
			return '2'
		return ''

	def populateRoundData(self, match, roundData, lastRound, lowerHeaders):
		id = self.getSimplifiedId(match['match2id'])
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
			opponent1 = self.getOpponent(param)
			winner1Param = param
			round['D'] = round['D'] + 1
		else:
			param = 'R' + str(round['R']) + 'W' + str(round['W'])
			#RxWx
			opponent1 = self.getOpponent(param, scoreKey= 'score2' if reset else 'score')
			winner1Param = param
			round['W'] = round['W'] + 1

		opponent2 = None
		winner2Param = ''
		if (not 'tolower' in bd) and not reset:
			param = 'R' + str(round['R']) + 'D' + str(round['D'])
			#RxDx
			opponent2 = self.getOpponent(param)
			winner2Param = param
			round['D'] = round['D'] + 1
		else:
			param = 'R' + str(round['R']) + 'W' + str(round['W'])
			#RxWx
			opponent2 = self.getOpponent(param, scoreKey= 'score2' if reset else 'score')
			winner2Param = param
			round['W'] = round['W'] + 1

		details = self.getDetails('R' + str(round['R']) + 'G' + str(round['G']), index = 1 if reset else 0)
		winner = self.getWinner(winner1Param, winner2Param)
		if winner:
			if not details:
				details = Template("FAKE")
			details.add('winner', winner)
		match2 = self.matchClass()(opponent1, opponent2, details)
		self.roundData[id] = match2
		roundData[round['R']] = round
		lastRound = round

		return roundData, lastRound, lowerHeaders

	def handleCustomMapping(self):
		for roundParam, match1Params in self.customMapping.items():
			reset = False
			if roundParam == RESET_MATCH:
				reset = True
			opp1param = match1Params["opp1"]
			opp2param = match1Params["opp2"]
			details = self.getDetails(match1Params["details"], index = 1 if reset else 0)
			opponent1 = self.getOpponent(opp1param, scoreKey= 'score2' if reset else 'score')
			opponent2 = self.getOpponent(opp2param, scoreKey= 'score2' if reset else 'score')
			winner = self.getWinner(opp1param, opp2param)
			if winner:
				if not details:
					details = Template("FAKE")
				details.add('winner', winner)
			match2 = self.matchClass()(opponent1, opponent2, details)
			self.roundData[roundParam] = match2

			if "header" in match1Params:
				header = get_parameter_str(self.template, match1Params["header"])
				if header:
					self.roundData[roundParam + 'header'] = header

	def process(self):
		if (self.template is None):
			return

		self.shortNames = get_parameter_str(self.template, 'shortNames')
		self.columnwidth = get_parameter_str(self.template, 'column-width')
		if not self.columnwidth:
			self.columnwidth = get_parameter_str(self.template, 'column-width1')

		roundData = {}
		lowerHeaders = {}
		lastRound = None
		#Mapping via lpdb template data
		for match in self.bracketData:
			roundData, lastRound, lowerHeaders = self.populateRoundData(match, roundData, lastRound, lowerHeaders)

		for n in range(1, lastRound['R'] + 1):
			headerUp = get_parameter_str(self.template, 'R' + str(n))
			if headerUp:
				self.roundData['R' + str(n) + 'M1header'] = headerUp
			headerLow = get_parameter_str(self.template, 'L' + str(n))
			if headerLow and (n in lowerHeaders):
				self.roundData['R' + str(n) + 'M' + str(lowerHeaders[n]) + 'header'] = headerLow
	
		if self.customMapping:
			self.handleCustomMapping()

	def __str__(self) -> str:
		out = '{{Bracket|'+ self.newTemplateId + '|id=' + generate_id()
		if self.shortNames:
			out = out + '|forceShortName=true'
		if self.columnwidth:
			out = out + '|matchWidth=' + self.columnwidth
			
		matchOut = ''
		roundOutputOrder = self.getRoundOutputOrder()
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
					if (not match.opponent1.score) and (not match.opponent2.score) and (get_parameter_str(match.template, 'winner') == None):
						continue
				header = ''
				if param == THIRD_PLACE_MATCH or param == RESET_MATCH:
					if param == THIRD_PLACE_MATCH:
						header = '\n\n' + '<!-- Third Place Match -->'
				elif 'header' in round:
					header = self.getHeader(round['header'])
				matchOut = matchOut + header
				matchOut = matchOut + '\n|' + param + '=' + str(match)

		return out + matchOut + '\n}}'