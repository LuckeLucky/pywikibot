from ..commons.bracket import Bracket as commonsBracket
from ..commons.opponent import Opponent, SoloOpponent

class Bracket(commonsBracket):
	def getSoloOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.getValue(key)
		link = self.getValue(key + 'link')
		flag = self.getValue(key + 'flag')
		race = self.getValue(key + 'race')
		score = self.getValue(key + scoreKey)

		return SoloOpponent(name = name, link = link, flag = flag, race = race, score = score)
