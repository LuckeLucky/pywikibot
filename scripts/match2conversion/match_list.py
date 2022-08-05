import random
import string

from .match import Match


class MatchList(object):

	def __init__(self) -> None:
		self.title = ''
		self.matchsection = ''
		self.width = ''
		self.collapsed = ''
		self.attached = ''
		self.gsl = ''

		self.headers = []
		self.matches = []

	def set_title(self, value: str) -> None:
		self.title = value

	def set_width(self, value: str) -> None:
		self.width = value

	def set_collapsed(self, value: str) -> None:
		self.collapsed = value

	def set_attached(self, value: str) -> None:
		self.attached = value

	def set_matchsection(self, value: str) -> None:
		self.matchsection = value

	def _generate_id(self):
		ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
		return ran

	def set_gsl(self, value):
		if value == 'winners':
			self.gsl = 'winnersfirst'
		elif value == 'losers':
			self.gsl = 'losersfirst'
		else:
			self.gsl = value

	def has_gsl(self) -> bool:
		return self.gsl == ''

	def add_match(self, match: Match) -> None:
		self.matches.append(match)

	def add_header(self, index: int, value: str) -> None:
		self.headers.append('|M' + str(index) + 'header=' + value)

	def __str__(self) -> str:
		out = '{{Matchlist|id=' + self.generateId()

		if self.width:
			out = out + '|width=' + self.width

		if self.attached:
			out = out + '|attached=' + self.attached

		if self.collapsed:
			out = out + '|collapsed=' + self.collapsed

		if self.gsl:
			out = out + '|gsl=' + self.collapsed

		if self.title:
			out = out + '|title=' + self.title

		if self.matchsection:
			out = out + '|matchsection=' + self.matchsection

		if self.headers:
			for header in self.headers:
				out = out + '\n' + header

		if self.matches:
			for matchIndex, match in enumerate(self.matches):
				out = out + '\n|M' + str(matchIndex + 1) + '=' + str(match)

		return out + '\n}}'