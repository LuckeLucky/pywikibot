from abc import abstractmethod
from mwparserfromhell.nodes import Template

from scripts.match2conversion.opponent import Opponent
from scripts.utils.parser_helper import get_value, sanitize_template

from .match import Match
from .helpers import generate_id

class MatchListAbstract(object):
	def __init__(self) -> None:
		self.title = ''
		self.matchsection = ''
		self.width = ''
		self.collapsed = ''
		self.attached = ''
		self.gsl = ''

		self.headers = []
		self.matches = []

	def get_opponent(self, matchMap: Template, opponentIndex: int) -> Opponent:
		teamName = get_value(matchMap, 'team' + str(opponentIndex))
		teamScore = get_value(matchMap, 'games' + str(opponentIndex))
		return Opponent(teamName, teamScore)

	def get_summary(self, matchMap: Template):
		if matchMap.has('details'):
			return sanitize_template(matchMap.get('details').value.filter_templates()[0])
		return None

	def get_gsl(self, template: Template):
		gsl = get_value(template, 'gsl')
		if gsl == 'winners':
			return 'winnersfirst'
		elif gsl == 'losers':
			return 'losersfirst'
		return gsl

	def add_header(self, index, value):
		self.headers.append('|M' + str(index) + 'header=' + value)

	@abstractmethod
	def get_winner(self, matchMap: Template) -> int:
		pass

	@abstractmethod
	def process(self):
		pass

	def __str__(self) -> str:
		out = '{{Matchlist|id=' + generate_id()

		if self.width:
			out = out + '|width=' + self.width

		if self.attached:
			out = out + '|attached=' + self.attached

		if self.collapsed:
			out = out + '|collapsed=' + self.collapsed

		if self.gsl:
			out = out + '|gsl=' + self.gsl

		if self.title:
			out = out + '|title=' + self.title

		if self.matchsection:
			out = out + '|matchsection=' + self.matchsection

		if self.headers:
			for header in self.headers:
				out = out + '\n' + header

		if self.matches:
			for _, match in enumerate(self.matches):
				out = out + '\n|' + str(match)

		return out + '\n}}'


class MatchList(MatchListAbstract):

	def __init__(self, matchListStart: Template, matchMaps: list) -> None:
		self.matchListStart = sanitize_template(matchListStart)
		self.matchMaps = matchMaps
		super().__init__()

	def get_winner(self, matchMap: Template) -> int:
		winner = get_value(matchMap, 'win')
		if winner in ['1', '2', '0']:
			return int(winner)
		elif winner == 'draw':
			return 0
		else:
			return -1

	def process(self):
		if self.matchListStart is None:
			return

		self.title = get_value(self.matchListStart, 'title')
		self.matchsection = get_value(self.matchListStart, 'matchsection')
		self.width = get_value(self.matchListStart, 'width')
		self.collapsed = get_value(self.matchListStart, 'hide')
		if not self.collapsed:
			uncollapsed = get_value(self.matchListStart, 'uncollapsed-maps')
			if uncollapsed:
				if uncollapsed == 'true':
					self.collapsed = 'false'
				elif uncollapsed == 'false':
					self.collapsed = 'true'

		self.attached = get_value(self.matchListStart, 'attached')
		#If attached to GroupTable the matches are collapsed
		if self.attached:
			self.collapsed = self.attached
		self.gsl = self.get_gsl(self.matchListStart)

		if self.matchMaps is None:
			return

		for matchMapIndex, matchMap in enumerate(self.matchMaps):
			matchMap = sanitize_template(matchMap)
			#date ouside of details count as header
			header = get_value(matchMap, 'date')
			if header:
				self.add_header(matchMapIndex+1, header)

			opponent1 = self.get_opponent(matchMap, 1)
			opponent2 = self.get_opponent(matchMap, 2)
			details = self.get_summary(matchMap)
			winner = self.get_winner(matchMap)

			match = Match(opponent1, opponent2, winner, details)
			match.process()
			self.matches.append(match)


class MatchListLegacy(MatchListAbstract):
	def __init__(self, matchList: Template) -> None:
		self.matchList = sanitize_template(matchList)
		super().__init__()

	def get_winner(self, matchMap: Template) -> int:
		winner = get_value(matchMap, 'winner')
		if winner in ['1', '2', '0']:
			return int(winner)
		elif winner == 'draw':
			return 0
		else:
			return -1

	def process(self):
		if self.matchList is None:
			return

		self.title = get_value(self.matchList, 'title')
		self.width = get_value(self.matchList, 'width')
		self.collapsed = get_value(self.matchList, 'hide')
		if not self.collapsed:
			uncollapsed = get_value(self.matchList, 'uncollapsed-maps')
			if uncollapsed:
				if uncollapsed == 'true':
					self.collapsed = 'false'
				elif uncollapsed == 'false':
					self.collapsed = 'true'

		self.attached = get_value(self.matchList, 'attached')
		#If attached to GroupTable the matches are collapsed
		if self.attached:
			self.collapsed = self.attached
		self.gsl = self.get_gsl(self.matchList)

		for param in self.matchList.params:
			paramName = str(param.name)
			if paramName.startswith('match'):
				matchMap = sanitize_template(param.value.filter_templates()[0])
				if not matchMap:
					continue

				header = get_value(matchMap, 'date')
				if header:
					self.add_header(int(paramName[-1]), header)

				opponent1 = self.get_opponent(matchMap, 1)
				opponent2 = self.get_opponent(matchMap, 2)
				details = self.get_summary(matchMap)
				winner = self.get_winner(matchMap)

				match = Match(opponent1, opponent2, winner, details)
				match.process()
				self.matches.append(match)