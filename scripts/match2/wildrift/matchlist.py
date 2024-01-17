from typing import List
from scripts.match2.commons.template import Template
from ..commons.matchlist import Matchlist
from .match import Match

MAX_NUM_MAPS = 10

class MatchlistWildRift(Matchlist):
	Match = Match

	def __init__(self, template: Template, matchTemplates: List[Template]):
		super().__init__(template, matchTemplates)
		self.args['patch'] = self.template.getValue('patch')

	def getMatch(self, matchTemplate: Template) -> Match:
		opp1 = self.getOpponent(matchTemplate, 'team', 'score1')
		opp2 = self.getOpponent(matchTemplate, 'team2', 'score2')
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


		for x in range(1, MAX_NUM_MAPS):
			key = 'map' + str(x) + 'win'
			mapxwin = matchTemplate.getValue(key)
			if mapxwin:
				details.add(key, mapxwin)

		return self.createMatch([opp1, opp2], details, winner)
