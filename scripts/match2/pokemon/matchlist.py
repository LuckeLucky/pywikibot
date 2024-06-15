from scripts.match2.commons.opponent import Opponent
from scripts.match2.commons.template import Template

from ..commons.matchlist import Matchlist as commonsMatchlist

MAX_NUM_MAPS = 20

class Matchlist(commonsMatchlist):
	def getSoloOpponent(self, template: Template, key: str, scoreKey: str) -> Opponent:
		val = template.getValue(key)
		val = val.replace('[[', '').replace(']]', '')
		val = val.replace("'", '')
		template.add(key, val)
		return super().getSoloOpponent(template, key, scoreKey)
	def getMatch(self, matchTemplate: Template):
		opp1, opp2 = None, None
		if matchTemplate.name == 'MatchMaps':
			opp1 = self.getOpponent(matchTemplate, 'team1', 'score1')
			opp2 = self.getOpponent(matchTemplate, 'team2', 'score2')
		elif matchTemplate.name == 'MatchMapsNew':
			opp1 = self.getOpponent(matchTemplate, 'p1', 'p1score')
			opp2 = self.getOpponent(matchTemplate, 'p2', 'p2score')

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

		if not details:
			details = Template.createFakeTemplate()

		for x in range(1, MAX_NUM_MAPS):
			key = f'map{x}'
			details.add(key + 'win', matchTemplate.getValue(key + 'win'))
			details.add(key + 'score', matchTemplate.getValue(key + 'score'))

		return self.createMatch([opp1, opp2], details, winner)
