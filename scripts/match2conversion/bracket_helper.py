import copy
import json
import re

from functools import cmp_to_key
from pathlib import Path

bracketAlias = {
	'2SETeamBracket': '2',
	'2SEBracket': '2',
	'4SETeamBracket': '4',
	'4SEBracket': '4',
	'8SETeamBracket': '8',
	'8SEBracket': '8',
	'4DETeamBracket': '4U2L1D',
	'32DETeamBracket': '32U16L8DSL4DSL2DSL1D',
	'8DETeamBracket': '8U4L2DSL1D'
}

class BracketHelpder(object):
	bracketData = None
	headersData = None
	mapping = None
	outputOrder = None

	@staticmethod
	def check_support(oldTemplateName: str) -> bool:
		"""
			Checks if the old template can be converted
		"""
		return oldTemplateName in bracketAlias

	@staticmethod
	def get_new_bracket_name(templateName: str) -> str:
		"""
			Returns the new Bracket name
		"""
		return 'Bracket/' + bracketAlias[templateName]

	@staticmethod
	def load_bracket_data(templateName: str):
		p = Path(__file__).with_name('bracket_templates.json')
		file = p.open()
		data = json.load(file)
		BracketHelpder.bracketData = data[templateName] if templateName in data else None


	@staticmethod
	def load_custom_mapping(templateName: str):
		p = Path(__file__).with_name('custom_mappings.json')
		file = p.open()
		data = json.load(file)
		BracketHelpder.mapping = data[templateName] if templateName in data else None

	@staticmethod
	def load_headers_data():
		p = Path(__file__).with_name('headers_data.json')
		file = p.open()
		data = json.load(file)
		BracketHelpder.headersData = data

	@staticmethod
	def load(templateName: str) -> bool:
		"""
			Load bracket data and custom mappings into memory
		"""
		if not BracketHelpder.check_support(templateName):
			return False
		
		newBracketName = BracketHelpder.get_new_bracket_name(templateName)
		BracketHelpder.load_bracket_data(newBracketName)
		BracketHelpder.load_headers_data()
		BracketHelpder.load_custom_mapping(newBracketName)

		return True

	@staticmethod
	def get_simplified_id(id: str) -> str:
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

	@staticmethod
	def get_round_output_order():
		if BracketHelpder.outputOrder:
			return BracketHelpder.outputOrder
		bracketDataList = []

		for match in BracketHelpder.bracketData:
			id = BracketHelpder.get_simplified_id(match['match2id'])
			bracketData = match['match2bracketdata']
			bracketData['matchKey'] = id
			bracketDataList.append(bracketData)

		def sortKey(bracketData):
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
		BracketHelpder.outputOrder = copy.copy(bracketDataList)

		return bracketDataList

	@staticmethod
	def get_header(headerCode: str) -> str:
		if not headerCode:
			return ''

		if headerCode in BracketHelpder.headersData:
			return '\n\n' + '<!-- ' + BracketHelpder.headersData[headerCode] + ' -->'
		
		return ''
