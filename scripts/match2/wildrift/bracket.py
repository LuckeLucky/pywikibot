from ..commons.bracket import Bracket as commonsBracket
from ..commons.opponent import Opponent, TeamOpponent
from scripts.match2.commons.template import Template

class Bracket(commonsBracket):
	def getTeamOpponent(self, template: Template, key: str, scoreKey: str) -> Opponent:
		name = template.get(key + 'team')
		score = template.get(key + scoreKey)
		if name:
			return TeamOpponent(name = name, score = score)
		wildriftname = template.get(key + 'wildrift')
		if wildriftname:
			return Opponent(name = wildriftname, score = score)
		return TeamOpponent()
