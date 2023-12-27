import copy
import json
from functools import cmp_to_key
from pathlib import Path
from typing import Dict, List

from .utils import generateId
from .template import Template
from .match import Match as commonsMatch
from .opponent import Opponent, SoloOpponent, TeamOpponent

MAX_NUMBER_OPPONENTS = 2
RESET_MATCH = 'RxMBR'
THIRD_PLACE_MATCH = 'RxMTP'

class Bracket:
	Match = commonsMatch
	isLoaded: bool = False
	bracketData: Dict[str, List] = {}
	headersData: Dict[str, str] = {}
	customMapping: Dict[str, List] = {}
	outputOrder: Dict[str, List] = {}

	def __init__(self, template: Template) -> None:
		if not self.isLoaded:
			self.load()
		self.template: Template = template
		self.roundData: Dict = {}
		self.newTemplateId: str = self.template.getValue(index=0)
		self.oldTemplateId: str = self.template.getValue(index=1)
		self.bracketType: str = self.template.getValue('type')
		self.id: str = self.template.getValue('id')
		if not self.id:
			self.id = generateId()
		self.mappingKey: str = self.newTemplateId + '$$' + self.oldTemplateId

	@classmethod
	def isBracketDataAvailable(cls, newTemplateId: str) -> bool:
		if not cls.isLoaded:
			cls.load()
		return newTemplateId in cls.bracketData

	@classmethod
	def loadBracketData(cls):
		filePath = Path(__file__).with_name('bracket_templates.json')
		with filePath.open(encoding='utf-8') as file:
			data = json.load(file)
			cls.bracketData = data

	@classmethod
	def loadHeadersData(cls):
		filePath = Path(__file__).with_name('headers_data.json')
		with filePath.open(encoding='utf-8') as file:
			data = json.load(file)
			cls.headersData = data

	@classmethod
	def loadCustomMapping(cls):
		pass

	@classmethod
	def load(cls):
		'''
			Load bracket data and custom mappings into memory
		'''
		cls.loadBracketData()
		cls.loadCustomMapping()
		cls.loadHeadersData()
		cls.isLoaded = True

	@classmethod
	def getSimplifiedId(cls, match2Id: str) -> str:

		'''
			Simplify round id
			ex. id = 'R01M001' return 'R1M1'
		'''
		match2Id = match2Id.split('_')[1] if len(match2Id.split('_')) > 1 else match2Id
		if match2Id == 'RxMTP':
			return match2Id
		elif match2Id == 'RxMBR':
			return match2Id
		else:
			match2Id = match2Id.replace('-', '')
			roundNumber, _, matchNumber = match2Id[1:].partition('M')
			return 'R' + str(int(roundNumber)) + 'M' + str(int(matchNumber))

	@classmethod
	def getHeader(cls, headerCode: str) -> str:
		if not headerCode:
			return ''

		if headerCode in cls.headersData:
			return '\n\n' + '<!-- ' + cls.headersData[headerCode] + ' -->'
		return ''

	@classmethod
	def getRoundOutputOrder(cls, newTemplateId: str):
		if newTemplateId in cls.outputOrder:
			return cls.outputOrder[newTemplateId]
		bracketDataList = []

		for match in cls.bracketData[newTemplateId]:
			simplifiedId = cls.getSimplifiedId(match['match2id'])
			bracketData = match['match2bracketdata']
			bracketData['matchKey'] = simplifiedId
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
		cls.outputOrder[newTemplateId] = copy.copy(bracketDataList)

		return bracketDataList

	@classmethod
	def isMatchValidResetOrThird(cls, match: Match, reset: bool, roundParam: str):
		if roundParam not in [THIRD_PLACE_MATCH, RESET_MATCH]:
			return True

		for opponent in match.opponents:
			if opponent.score:
				return True

		for key, _ in match.template.iterateParams(True):
			if key != 'winner':
				return True
			if key == 'winner' and not reset:
				return True
		return False

	def getTeamOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.template.getValue(key + 'team')
		score = self.template.getValue(key + scoreKey)
		if name:
			return TeamOpponent(name, score)
		return TeamOpponent()

	def getSoloOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.template.getValue(key)
		flag = self.template.getValue(key + 'flag')
		score = self.template.getValue(key + scoreKey)
		if (name is None) and (score is None) and (flag is None):
			return SoloOpponent()
		return SoloOpponent(name, score, '', flag)

	def getOpponent(self, key: str, scoreKey: str = 'score') -> Opponent:
		opponentGet = getattr(self, 'get' + str(self.bracketType).capitalize() + 'Opponent')
		if not opponentGet:
			raise ValueError(self.bracketType + 'is not supported')
		return opponentGet(key, scoreKey)

	def getDetails(self, key, index = 0):
		if self.template.has(key + 'details'):
			templates = self.template.get(key + 'details').value.filter_templates(recursive = False)
			if len(templates) > index:
				return Template(templates[index])
		return None

	def getWinner(self, team1Key: str, team2Key) -> int:
		if self.template.getValue(team1Key + 'win'):
			return '1'
		if self.template.getValue(team2Key + 'win'):
			return '2'
		return ''

	def populateRoundData(self, match, roundData, lastRound, lowerHeaders):
		simplifiedId = self.getSimplifiedId(match['match2id'])
		roundNumber, _, _ = simplifiedId[1:].partition('M')
		if roundNumber.isnumeric():
			roundNumber = int(roundNumber)
		reset = False
		if simplifiedId == THIRD_PLACE_MATCH:
			currentRound = lastRound
		elif simplifiedId == RESET_MATCH:
			currentRound = lastRound
			currentRound['G'] = currentRound['G'] - 2
			currentRound['W'] = currentRound['W'] - 2
			currentRound['D'] = currentRound['D'] - 2
			reset = True
		else:
			if roundNumber in roundData:
				currentRound = roundData[roundNumber]
			else:
				currentRound = {'R': roundNumber, 'G': 0, 'D': 1, 'W': 1}
		currentRound['G'] = currentRound['G'] + 1

		bd = match['match2bracketdata']

		if 'header' in bd:
			if bd['header'].startswith('!l'):
				lowerHeaders[roundNumber] = currentRound['G']

		opponents: List[Opponent] = []
		winnerParams: List[str] = []

		for opponentIndex in range(MAX_NUMBER_OPPONENTS):
			param = None
			if (not reset and
				(not 'toupper' in bd and opponentIndex == 0 or
				not 'tolower' in bd and opponentIndex == 1)):
				param = 'R' + str(currentRound['R']) + 'D' + str(currentRound['D'])
				currentRound['D'] = currentRound['D'] + 1
			else:
				param = 'R' + str(currentRound['R']) + 'W' + str(currentRound['W'])
				currentRound['W'] = currentRound['W'] + 1

			opponents.append(self.getOpponent(param, scoreKey= 'score2' if reset else 'score'))
			winnerParams.append(param)

		details = self.getDetails('R' + str(currentRound['R']) + 'G' + str(currentRound['G']), index = 1 if reset else 0)
		winner = self.getWinner(winnerParams[0], winnerParams[1])
		if winner:
			if not details:
				details = Template.createFakeTemplate()
			details.add('winner', winner)
		match2 = self.Match(opponents, details)
		match2.isValidResetOrThird = self.isMatchValidResetOrThird(match2, reset, simplifiedId)
		self.roundData[simplifiedId] = match2
		roundData[currentRound['R']] = currentRound
		lastRound = currentRound

		return roundData, lastRound, lowerHeaders

	def handleCustomMapping(self):
		for roundParam, match1Params in self.customMapping[self.mappingKey].items():
			reset = False
			if roundParam == RESET_MATCH:
				reset = True

			if 'header' in match1Params:
				header = self.template.getValue(match1Params['header'])
				if header:
					self.roundData[roundParam + 'header'] = header

			opp1param = match1Params['opp1']
			opp2param = match1Params['opp2']
			details = self.getDetails(match1Params['details'], index = 1 if reset else 0)
			winner = self.getWinner(opp1param, opp2param)
			if winner:
				if not details:
					details = Template.createFakeTemplate()
				details.add('winner', winner)
			opponent1 = self.getOpponent(opp1param, scoreKey= 'score2' if reset else 'score')
			opponent2 = self.getOpponent(opp2param, scoreKey= 'score2' if reset else 'score')
			match2 = self.Match([opponent1, opponent2], details)
			match2.isValidResetOrThird = self.isMatchValidResetOrThird(match2, reset, roundParam)
			self.roundData[roundParam] = match2

	def process(self):
		if self.template is None:
			return

		roundData = {}
		lowerHeaders = {}
		lastRound = None
		#Mapping via lpdb template data
		for match in self.bracketData[self.newTemplateId]:
			roundData, lastRound, lowerHeaders = self.populateRoundData(match, roundData, lastRound, lowerHeaders)

		for n in range(1, lastRound['R'] + 1):
			headerUp = self.template.getValue('R' + str(n))
			if headerUp:
				self.roundData['R' + str(n) + 'M1header'] = headerUp
			headerLow = self.template.getValue('L' + str(n))
			if headerLow and (n in lowerHeaders):
				self.roundData['R' + str(n) + 'M' + str(lowerHeaders[n]) + 'header'] = headerLow

		if self.mappingKey in self.customMapping:
			self.handleCustomMapping()

	def __str__(self) -> str:
		out = '{{Bracket|'+ self.newTemplateId + '|id=' + self.id
		matchOut = ''
		roundOutputOrder = self.getRoundOutputOrder(self.newTemplateId)
		for currentRound in roundOutputOrder:
			param = currentRound['matchKey']
			if param + 'header' in self.roundData:
				out = out + '\n|' + param + 'header=' + self.roundData[param + 'header']

			if not param in self.roundData:
				if param != THIRD_PLACE_MATCH and param != RESET_MATCH:
					matchOut = matchOut + '\n|' + param + '=' + '\n'
				continue
			match: commonsMatch = self.roundData[param]
			if param in [THIRD_PLACE_MATCH, RESET_MATCH] and not match.isValidResetOrThird:
				continue
			header = ''
			if param == THIRD_PLACE_MATCH:
				header = '\n\n' + '<!-- Third Place Match -->'
			elif 'header' in currentRound:
				header = self.getHeader(currentRound['header'])
			matchOut = matchOut + header
			matchOut = matchOut + '\n|' + param + '=' + str(match)

		return out + matchOut + '\n}}'
