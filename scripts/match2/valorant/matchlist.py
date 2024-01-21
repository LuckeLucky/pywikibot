from typing import List
from scripts.match2.commons.template import Template

from ..commons.matchlist import Matchlist as commonsMatchlist
from .match import Match

class Matchlist(commonsMatchlist):
	Match = Match

	def __init__(self, template: Template, matchTemplates: List[Template]):
		super().__init__(template, matchTemplates)
		self.args['matchsection'] = self.template.getValue('matchsection')

	def getMatch(self, matchTemplate: Template) -> Match:
		opp1 = self.getOpponent(matchTemplate, 'team1', 'games1')
		opp2 = self.getOpponent(matchTemplate, 'team2', 'games2')
		details = self.getDetails(matchTemplate, 'details')
		winner = matchTemplate.getValue('winner')
		walkover = matchTemplate.getValue('walkover')
		if walkover:
			if walkover == '1':
				opp1.score = 'W'
				opp2.score = 'FF'
				winner = '1'
			if walkover == '2':
				opp1.score = 'FF'
				opp2.score = 'W'
				winner = '2'

		return self.createMatch([opp1, opp2], details, winner)
