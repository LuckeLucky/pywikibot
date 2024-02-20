from typing import Dict, List
from .template import Template
from .match import Match as commonsMatch
from .opponent import Opponent, SoloOpponent, TeamOpponent
from .utils import importClass

GSL_GF = 'gf'
GSL_WINNERS = 'winners'
GSL_LOSERS = 'losers'

class Matchlist:
	language: str = None
	matchClass: commonsMatch = None

	def __init__(self, template: Template, matchTemplates: List[Template]):
		if self.matchClass is None:
			self.matchClass = importClass(self.language, 'Match')
		self.template: Template = template
		self.data: Dict[str, commonsMatch | str] = {}
		self.bracketType: str = 'team'

		self.matchTemplates: List[Template] = matchTemplates
		self.args: Dict[str, str] = {}
		self.args['id'] = self.template.getValue('id')
		self.args['title'] = self.template.getValue('title')
		self.args['width'] = self.template.getValue('width')
		if self.template.getBool('hide'):
			self.args['collapsed'] = 'true'
			self.args['attached'] = 'true'

		self.args['gsl'] = self.getGsl(self.template.getValue('gsl'))

	def getGsl(self, gsl: str) -> str:
		if not gsl:
			return ''
		if gsl.startswith(GSL_GF):
			self.data['M6header'] = 'Grand Final'
		if gsl.endswith(GSL_WINNERS):
			return 'winnersfirst'
		if gsl.endswith(GSL_LOSERS):
			return 'losersfirst'
		return ''

	def getTeamOpponent(self, template: Template, key: str, scoreKey: str) -> Opponent:
		name = template.getValue(key)
		score = template.getValue(scoreKey)
		if name:
			return TeamOpponent(name, score)
		return TeamOpponent()

	def getSoloOpponent(self, template: Template, key: str, scoreKey: str) -> Opponent:
		name = template.getValue(key)
		score = template.getValue(scoreKey)
		flag = template.getValue(key + 'flag')
		if name:
			return SoloOpponent(name, score, '', flag)
		return SoloOpponent()

	def getOpponent(self, template: Template, key: str, scoreKey) -> Opponent:
		opponentGet = getattr(self, 'get' + str(self.bracketType).capitalize() + 'Opponent')
		if not opponentGet:
			raise ValueError(self.bracketType + 'is not supported')
		return opponentGet(template, key, scoreKey)

	def getDetails(self, template: Template, key) -> Template:
		details = template.getNestedTemplate(key)
		if details:
			return Template(details)
		return None

	def createMatch(self, opponents: List[Opponent], details : Template, winner: str) -> commonsMatch:
		if winner:
			if not details:
				details = Template.createFakeTemplate()
			details.add('winner', winner)
		match = self.matchClass(opponents, details)
		return match

	def getMatch(self, matchTemplate: Template) -> commonsMatch:
		opp1 = self.getOpponent(matchTemplate, 'team1', 'score1')
		opp2 = self.getOpponent(matchTemplate, 'team2', 'score2')
		details = self.getDetails(matchTemplate, 'details')
		winner = matchTemplate.getValue('winner')

		return self.createMatch([opp1, opp2], details, winner)

	def populateData(self):
		for matchIndex, matchTemplate in enumerate(self.matchTemplates):
			matchParam = f'M{matchIndex+1}'
			header = matchTemplate.getValue('date') or matchTemplate.getValue('header')
			if header:
				self.data[f'{matchParam}header'] = header
			self.data[matchParam] = self.getMatch(matchTemplate)

	def __str__(self) -> str:
		self.populateData()

		out = '{{Matchlist'

		for key, value in self.args.items():
			if value:
				out += f'|{key}={value}'
		out += '\n'

		matchesOut = ''
		for key, value in self.data.items():
			if 'header' in key:
				out += f'|{key}={value}\n'
			else:
				matchesOut += '|' + str(value) + '\n'

		out += matchesOut

		out += '}}'

		return out
