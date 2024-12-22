from scripts.match2.commons.template import Template

from ..commons.matchlist import Matchlist as commonsMatchlist

MAX_NUM_MAPS = 10

class Matchlist(commonsMatchlist):
	def getMatch(self, matchTemplate: Template):
		opp1 = self.getOpponent(matchTemplate, 'team1dota', 'score1')
		opp2 = self.getOpponent(matchTemplate, 'team2dota', 'score2')
		details = self.getDetails(matchTemplate, 'details')
		winner = matchTemplate.get('winner')

		for x in range(1, MAX_NUM_MAPS):
			key = 'map' + str(x) + 'win'
			mapxwin = matchTemplate.get(key)
			if mapxwin:
				details.add(key, mapxwin)

		return self.createMatch([opp1, opp2], details, winner)
