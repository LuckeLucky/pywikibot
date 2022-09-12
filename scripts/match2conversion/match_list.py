from mwparserfromhell.nodes import Template

from scripts.match2conversion.opponent import Opponent
from scripts.utils.parser_helper import get_value, sanitize_template

from .match import Match
from .helpers import generate_id

class MatchList(object):

	def __init__(self, matchListStart: Template, matchMaps: list) -> None:
		self.matchListStart = sanitize_template(matchListStart)
		self.matchMaps = matchMaps

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

	def get_winner(self, matchMap: Template) -> int:
		winner = get_value(matchMap, 'win')
		if winner in ['1', '2', '0']:
			return int(winner)
		elif winner == 'draw':
			return 0
		else:
			return -1

	def get_gsl(self):
		gsl = get_value(self.matchListStart, 'gsl')
		if gsl == 'winners':
			return 'winnersfirst'
		elif gsl == 'losers':
			return 'losersfirst'
		return gsl

	def add_header(self, index, value):
		self.headers.append('|M' + str(index) + 'header=' + value)

	def process(self):
		if self.matchListStart is None:
			return

		self.title = get_value(self.matchListStart, 'title')
		self.matchsection = get_value(self.matchListStart, 'matchsection')
		self.width = get_value(self.matchListStart, 'width')
		self.collapsed = get_value(self.matchListStart, 'hide')
		self.attached = get_value(self.matchListStart, 'attached')
		#If attached to GroupTable the matches are collapsed
		if self.attached:
			self.collapsed = self.attached
		self.gsl = self.get_gsl()

		if self.matchMaps is None:
			return

		for matchMapIndex, matchMap in enumerate(self.matchMaps):
			matchMap = sanitize_template(matchMap)
			#date ouside of details count as header
			header = get_value(matchMap, 'date')
			if header:
				self.add_header(matchMapIndex, header)

			opponent1 = self.get_opponent(matchMap, 1)
			opponent2 = self.get_opponent(matchMap, 2)
			details = self.get_summary(matchMap)
			winner = self.get_winner(matchMap)

			match = Match(opponent1, opponent2, winner, details)
			match.process()
			self.matches.append(match)

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