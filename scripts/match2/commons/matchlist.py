from typing import Dict, List
from .template import Template
from .opponent import TeamOpponent
from .match import Match

MAX_NUM_MAPS = 10

class Matchlist:
	Match = Match
	def __init__(self, template: Template, matchTemplates: List[Template]):
		self.template: Template = template
		self.matchTemplates: List[Template] = matchTemplates
		self.args: Dict[str, str] = {}
		self.headers: Dict[str, str] = {}
		self.matches: List[Match] = []

	def process(self):
		if self.template is None:
			return

		self.args['id'] = self.template.getValue('id')
		self.args['title'] = self.template.getValue('title')
		self.args['width'] = self.template.getValue('width')
		hide = self.template.getValue('hide')
		if hide in ['true', 't', 'yes', 'y', '1']:
			self.args['collapsed'] = 'true'
			self.args['attached'] = 'true'

		for matchIndex, matchTemplate in enumerate(self.matchTemplates):
			sanitizedMatch = Template(matchTemplate)
			opp1 = TeamOpponent(sanitizedMatch.getValue('team1'), sanitizedMatch.getValue('score1'))
			opp2 = TeamOpponent(sanitizedMatch.getValue('team2'), sanitizedMatch.getValue('score2'))
			winner = sanitizedMatch.getValue('winner')
			details = sanitizedMatch.getNestedTemplate('details')

			header = sanitizedMatch.getValue('date')
			if header:
				self.headers['M' + str(matchIndex+1) + 'header'] = header

			if winner:
				if not details:
					details = Template("FAKE")
			details.add('winner', winner)

			walkover = sanitizedMatch.getValue('walkover')
			if walkover:
				if walkover == '1':
					opp1.score = 'W'
					opp2.score = 'FF'
					details.add('winner', '1')
				if walkover == '2':
					opp1.score = 'FF'
					opp2.score = 'W'
					details.add('winner', '2')

			for x in range(MAX_NUM_MAPS):
				key = 'map' + str(x) + 'win'
				mapxwin = sanitizedMatch.getValue(key)
				if mapxwin:
					details.add(key, mapxwin)

			self.matches.append(self.Match([opp1, opp2], details))

	def __str__(self) -> str:
		out = '{{Matchlist'

		for key, value in self.args.items():
			out += f'|{key}={value}'
		out += '\n'

		for key, value in self.headers.items():
			out += f'|{key}={value}\n'

		for match in self.matches:
			out += '|' + str(match) + '\n'

		out += '\n}}'

		return out
