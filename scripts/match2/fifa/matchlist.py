from typing import List
from scripts.match2.commons.opponent import Opponent
from scripts.match2.commons.template import Template

from ..commons.matchlist import Matchlist as commonsMatchlist

MAX_NUMBER_OF_MAPS = 10

class Matchlist(commonsMatchlist):
	def createMatch(self, opponents: List[Opponent], details : Template, winner: str):
		if winner:
			if not details:
				details = Template.createFakeTemplate()
			details.add('winner', winner)
		match = self.matchClass(opponents, details)
		return match

	def getMatch(self, matchTemplate: Template):
		opp1, opp2 = None, None
		if matchTemplate.name == 'MatchMaps2':
			opp1 = self.getOpponent(matchTemplate, 'team1', 'team1score')
			opp2 = self.getOpponent(matchTemplate, 'team2', 'team2score')
		elif matchTemplate.name == 'MatchMaps':
			opp1 = self.getOpponent(matchTemplate, 'p1', 'p1score')
			opp2 = self.getOpponent(matchTemplate, 'p2', 'p2score')
		else:
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

		if not opp1.score and not opp2.score and matchTemplate.has('map1win'):
			scores = [0, 0]
			for x in range(1, MAX_NUMBER_OF_MAPS):
				mapxwin = matchTemplate.getValue('map' + str(x) + 'win')
				if mapxwin == '1':
					scores[0] = scores[0] + 1
				elif mapxwin == '2':
					scores[1] = scores[1] + 1
			opp1.score = str(scores[0])
			opp2.score = str(scores[1])

		return self.createMatch([opp1, opp2], details, winner)
