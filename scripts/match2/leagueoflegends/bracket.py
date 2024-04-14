from ..commons.bracket import Bracket as commonsBracket
from ..commons.opponent import Opponent, TeamOpponent

class Bracket(commonsBracket):
	def getTeamOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.template.getValue(key + 'team')
		score = self.template.getValue(key + scoreKey)
		if name:
			return TeamOpponent(name = name, score = score)
		leagueName = self.template.getValue(key + 'league')
		if leagueName:
			return Opponent(name = leagueName, score = score)
		return TeamOpponent()
