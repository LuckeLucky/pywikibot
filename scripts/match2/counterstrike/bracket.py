from ..commons.bracket import Bracket as commonsBracket
from ..commons.opponent import Opponent, TeamOpponent

class Bracket(commonsBracket):
	def getTeamOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.getValue(key + 'team')
		score = self.getValue(key + scoreKey)
		if name:
			return TeamOpponent(name = name, score = score)
		csName = self.getValue(key)
		if csName:
			return Opponent(name = csName, score = score)
		return TeamOpponent()
