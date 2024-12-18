from typing import Dict, List

import pywikibot
import os

import copy
import json
from functools import cmp_to_key

absolutePath = os.path.abspath
joinPath = os.path.join

RESET_MATCH = 'RxMBR'
THIRD_PLACE_MATCH = 'RxMTP'
MAX_NUMBER_OPPONENTS = 2

class BracketDataManager:
	def __init__(self, language: str) -> None:
		self.language = language

		self.bracketData: Dict[str, List] = {}
		self.customMapping: Dict[str, List] = {}
		self.headersData: Dict[str, str] = {}

		self.defaultMapping: Dict[str, List] = {}
		self.outputOrder: Dict[str, List] = {}
		self.load()

	def loadBracketData(self) -> None:
		path = absolutePath(os.path.dirname(__file__))
		path = joinPath(path, 'bracket_templates.json')
		with open(path, encoding='utf-8') as file:
			data = json.load(file)
			self.bracketData = data

	def loadCustomMapping(self) -> None:
		path = absolutePath(os.path.dirname(__file__))
		path = path.replace('commons', self.language)
		path = joinPath(path, 'bracket_custom_mappings.json')
		if os.path.isfile(path):
			with open(path, encoding='utf-8') as file:
				data = json.load(file)
				self.customMapping = data
		else:
			self.customMapping = {}

	def loadHeadersData(self):
		path = absolutePath(os.path.dirname(__file__))
		path = joinPath(path, 'headers_data.json')
		with open(path, encoding='utf-8') as file:
			data = json.load(file)
			self.headersData = data

	def load(self) -> None:
		'''
			Load bracket data and custom mappings into memory
		'''
		self.loadBracketData()
		self.loadCustomMapping()
		self.loadHeadersData()

	def loadFromCommons(self, templateId: str) -> bool:
		site = pywikibot.Site('commons', 'liquipedia')
		expandedText = site.expand_text("{{#invoke:Sandbox/LuckeLucky|main|" + templateId + "}}")
		loaded = json.loads(expandedText)
		if not loaded:
			return False
		self.bracketData[templateId] = loaded
		path = absolutePath(os.path.dirname(__file__))
		path = joinPath(path, 'bracket_templates.json')
		with open(path, 'w', encoding='utf-8') as file:
			json.dump(self.bracketData, file, ensure_ascii=False, indent=4)
		return True

	def isTemplateSupported(self, templateId: str) -> bool:
		if not templateId in self.bracketData:
			return self.loadFromCommons(templateId)
		return templateId in self.bracketData

	def getSimplifiedId(self, match2Id: str) -> str:

		'''
			Simplify round id
			ex. id = 'R01M001' return 'R1M1'
		'''
		match2Id = match2Id.split('_')[1] if len(match2Id.split('_')) > 1 else match2Id
		if match2Id in [THIRD_PLACE_MATCH, RESET_MATCH]:
			return match2Id

		match2Id = match2Id.replace('-', '')
		roundNumber, _, matchNumber = match2Id[1:].partition('M')
		return 'R' + str(int(roundNumber)) + 'M' + str(int(matchNumber))

	def getHeader(self, headerCode: str) -> str:
		if not headerCode:
			return ''

		if headerCode in self.headersData:
			return '\n\n' + '<!-- ' + self.headersData[headerCode] + ' -->'
		return ''

	def getRoundOutputOrder(self, templateId: str):
		if templateId in self.outputOrder:
			return self.outputOrder[templateId]
		bracketDataList = []

		for match in self.bracketData[templateId]:
			simplifiedId = self.getSimplifiedId(match['match2id'])
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
		self.outputOrder[templateId] = copy.copy(bracketDataList)

		return bracketDataList

	def loadDefaultMapping(self, templateId: str):
		defaultMapping = {}
		roundData = {}
		lowerHeaders = {}
		lastRound = None
		#Mapping via lpdb template data
		for match in self.bracketData[templateId]:
			roundData, lastRound, lowerHeaders = self.populateRoundData(
				defaultMapping, match, roundData, lastRound, lowerHeaders)

		for n in range(1, lastRound['R'] + 1):
			roundParam = f'R{n}M1'
			defaultMapping[roundParam]['header'] = f'R{n}'
			if n in lowerHeaders:
				roundParam = f'R{n}M{lowerHeaders[n]}'
				defaultMapping[roundParam]['header'] = f'L{n}'

		self.defaultMapping[templateId] = defaultMapping

	def populateRoundData(self, defaultMapping: Dict, match, roundData, lastRound, lowerHeaders):
		roundParam = self.getSimplifiedId(match['match2id'])
		roundNumber, _, _ = roundParam[1:].partition('M')
		if roundNumber.isnumeric():
			roundNumber = int(roundNumber)
		reset = False
		if roundParam == THIRD_PLACE_MATCH:
			currentRound = lastRound
		elif roundParam == RESET_MATCH:
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

		matchParams = {}
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
			matchParams['opp' + str(opponentIndex+1)] = param

		matchParams['details'] = 'R' + str(currentRound['R']) + 'G' + str(currentRound['G'])

		defaultMapping[roundParam] = matchParams
		roundData[currentRound['R']] = currentRound
		lastRound = currentRound

		return roundData, lastRound, lowerHeaders
