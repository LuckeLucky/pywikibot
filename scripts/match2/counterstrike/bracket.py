from ..commons.bracket import Bracket as commonsBracket
from ..commons.opponent import Opponent, TeamOpponent

class Bracket(commonsBracket):
	def getTeamOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.template.getValue(key + 'team')
		score = self.template.getValue(key + scoreKey)
		if name:
			return TeamOpponent(name = name, score = score)
		csName = self.template.getValue(key)
		if csName:
			return Opponent(name = csName, score = score)
		return TeamOpponent()
