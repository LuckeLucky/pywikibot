from ..commons.bracket import Bracket as commonsBracket

class Bracket(commonsBracket):
	def getWinner(self, team1Key: str, team2Key) -> str:
		if str(self.bracketType).lower() == 'solo' and team1Key[0] in ['r', 'l']:
			key = team1Key[:-2] + 'win'
			return self.template.getValue(key)
		return super().getWinner(team1Key, team2Key)
