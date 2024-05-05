from scripts.match2.commons.opponent import SoloOpponent
from scripts.match2.commons.template import Template

from ..commons.matchlist import Matchlist as commonsMatchlist

class Matchlist(commonsMatchlist):
	def getSoloOpponent(self, template: Template, key: str, scoreKey: str) -> SoloOpponent:
		name = template.getValue(key)
		link = template.getValue(key + 'link')
		flag = template.getValue(key + 'flag')
		race = template.getValue(key + 'race')
		score = template.getValue(scoreKey)

		return SoloOpponent(name = name, link = link, flag = flag, race = race, score = score)


	def getMatch(self, matchTemplate: Template):
		opp1 = self.getOpponent(matchTemplate, 'player1', 'player1score')
		opp2 = self.getOpponent(matchTemplate, 'player2', 'player2score')
		winner = matchTemplate.getValue('winner')

		return self.createMatch([opp1, opp2], matchTemplate, winner)
