from typing import Dict, List
from .template import Template
from .matchgroup import MatchGroup
from .match import Match as commonsMatch
from .opponent import Opponent
from .utils import importClass

GSL_GF = 'gf'
GSL_WINNERS = 'winners'
GSL_LOSERS = 'losers'

class Matchlist(MatchGroup):
	language: str = None
	matchClass: commonsMatch = None

	def __init__(self, template: Template, matchTemplates: List[Template]) -> None:
		if self.matchClass is None:
			self.matchClass = importClass(self.language, 'Match')
		super().__init__(template)
		self.data: Dict[str, commonsMatch | str] = {}

		self.matchTemplates: List[Template] = matchTemplates
		self.args: Dict[str, str] = {}
		self.args['id'] = self.getValue('id')
		self.args['title'] = self.getValue('title') or self.getValue('1')
		self.args['width'] = self.getValue('width')
		if self.template.getBool('hide'):
			self.args['collapsed'] = 'true'
			self.args['attached'] = 'true'

		self.args['gsl'] = self.getGsl(self.getValue('gsl'))

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

	def getDetails(self, template: Template, key) -> Template:
		return template.getNestedTemplate(key)

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
		winner = matchTemplate.get('winner')

		return self.createMatch([opp1, opp2], details, winner)

	def populateData(self) -> None:
		for matchIndex, matchTemplate in enumerate(self.matchTemplates):
			matchParam = f'M{matchIndex+1}'
			header = matchTemplate.get('date') or matchTemplate.get('header')
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
