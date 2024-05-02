from ..commons.bracket import Bracket as commonsBracket
from ..commons.opponent import Opponent, SoloOpponent

class Bracket(commonsBracket):
	def getSoloOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.template.getValue(key)
		link = self.template.getValue(key + 'link')
		flag = self.template.getValue(key + 'flag')
		race = self.template.getValue(key + 'race')
		score = self.template.getValue(key + scoreKey)

		return SoloOpponent(name = name, link = link, flag = flag, race = race, score = score)
