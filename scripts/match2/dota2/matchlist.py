from typing import List
from scripts.match2.commons.opponent import Opponent, TeamOpponent
from scripts.match2.commons.template import Template

from ..commons.matchlist import Matchlist as commonsMatchlist

class Matchlist(commonsMatchlist):
	def __init__(self, template: Template, matchTemplates: List[Template]):
		super().__init__(template, matchTemplates)
		self.args['matchsection'] = self.template.getValue('matchsection')

	def getTeamOpponent(self, template: Template, key: str, scoreKey: str) -> Opponent:
		name = template.getValue(key)
		score = template.getValue(scoreKey)
		if name:
			return TeamOpponent(name = name, score = score)
		name = template.getValue(key + 'dota')
		if name:
			return Opponent(name = name, score = score)
		return TeamOpponent()

	def getMatch(self, matchTemplate: Template):
		opp1 = self.getOpponent(matchTemplate, 'player1' if matchTemplate.has('player1') else 'team1', 'score1')
		opp2 = self.getOpponent(matchTemplate, 'player2' if matchTemplate.has('player2') else 'team2', 'score2')
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

		for key, value in matchTemplate.iterateByPrefix('map', ignoreEmpty=True):
			details.add(key, value)

		return self.createMatch([opp1, opp2], details, winner)
