from ..commons.bracket import Bracket as commonsBracket
from ..commons.opponent import Opponent, TeamOpponent

class Bracket(commonsBracket):
	def getTeamOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.template.getValue(key + 'team')
		score = self.template.getValue(key + scoreKey)
		if name:
			return TeamOpponent(name = name, score = score)
		wildRiftName = self.template.getValue(key + 'wildrift')
		if wildRiftName:
			return Opponent(name = wildRiftName, score = score)
		return TeamOpponent()