from typing import Dict, List

from .template import Template
from .match import Match as commonsMatch
from .opponent import Opponent, SoloOpponent, TeamOpponent

from .bracket_data_manager import BracketDataManager
from .utils import importClass

MAX_NUMBER_OPPONENTS = 2
RESET_MATCH = 'RxMBR'
THIRD_PLACE_MATCH = 'RxMTP'

class Bracket:
	language: str = None
	matchClass: commonsMatch = None
	bDM: BracketDataManager = None

	@classmethod
	def isMatchValidResetOrThird(cls, match: commonsMatch, reset: bool, roundParam: str):
		if roundParam not in [THIRD_PLACE_MATCH, RESET_MATCH]:
			return True

		for opponent in match.opponents:
			if opponent.score:
				return True

		for key, value in match.template.iterateParams(True):
			if value:
				if key != 'winner':
					return True
				if key == 'winner' and not reset:
					return True
		return False

	def __init__(self, template: Template) -> None:
		if self.bDM is None:
			self.bDM = BracketDataManager(self.language)
		if self.matchClass is None:
			self.matchClass = importClass(self.language, 'Match')
		self.template: Template = template
		self.data: Dict[str, commonsMatch | str] = {}

		self.newTemplateId: str = self.template.getValue('1')
		self.oldTemplateId: str = self.template.getValue('2')
		self.bracketType: str = self.template.getValue('type')
		self.bracketid: str = self.template.getValue('id')
		self.mappingKey: str = self.newTemplateId + '$$' + self.oldTemplateId

		if self.newTemplateId not in self.bDM.defaultMapping:
			self.bDM.loadDefaultMapping(self.newTemplateId)

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

	def getWinner(self, team1Key: str, team2Key) -> str:
		if self.template.getValue(team1Key + 'win'):
			return '1'
		if self.template.getValue(team2Key + 'win'):
			return '2'
		return ''

	def createMatch(self, opponents: List[Opponent], details : Template, winner: str) -> matchClass:
		if winner:
			if not details:
				details = Template.createFakeTemplate()
			details.add('winner', winner)
		match = self.matchClass(opponents, details)
		return match

	def _populateData(self, mapping: Dict[str, Dict[str, str] | str]):
		for roundParam, match1Params in mapping.items():
			reset = False
			if roundParam == RESET_MATCH:
				reset = True

			if 'header' in match1Params:
				header = self.template.getValue(match1Params['header'])
				if header:
					self.data[roundParam + 'header'] = header

			opp1param = match1Params['opp1']
			opp2param = match1Params['opp2']

			opponent1 = self.getOpponent(opp1param, scoreKey= 'score2' if reset else 'score')
			opponent2 = self.getOpponent(opp2param, scoreKey= 'score2' if reset else 'score')
			details = self.getDetails(match1Params['details'], index = 1 if reset else 0)
			winner = self.getWinner(opp1param, opp2param)
			match = self.createMatch([opponent1, opponent2], details, winner)
			match.isValidResetOrThird = self.isMatchValidResetOrThird(match, reset, roundParam)
			self.data[roundParam] = match

	def populateData(self):
		self._populateData(self.bDM.defaultMapping[self.newTemplateId])
		if self.mappingKey in self.bDM.customMapping:
			self._populateData(self.bDM.customMapping[self.mappingKey])

	def __str__(self) -> str:
		self.populateData()

		out = '{{Bracket|'+ self.newTemplateId + '|id=' + self.bracketid
		matchOut = ''
		roundOutputOrder = self.bDM.getRoundOutputOrder(self.newTemplateId)
		for currentRound in roundOutputOrder:
			param = currentRound['matchKey']
			if param + 'header' in self.data:
				out = out + '\n|' + param + 'header=' + self.data[param + 'header']

			if not param in self.data:
				if param != THIRD_PLACE_MATCH and param != RESET_MATCH:
					matchOut = matchOut + '\n|' + param + '=' + '\n'
				continue
			match: commonsMatch = self.data[param]
			if param in [THIRD_PLACE_MATCH, RESET_MATCH] and not match.isValidResetOrThird:
				continue
			header = ''
			if param == THIRD_PLACE_MATCH:
				header = '\n\n' + '<!-- Third Place Match -->'
			elif 'header' in currentRound:
				header = self.bDM.getHeader(currentRound['header'])
			matchOut = matchOut + header
			matchOut = matchOut + '\n|' + param + '=' + str(match)

		return out + matchOut + '\n}}'
