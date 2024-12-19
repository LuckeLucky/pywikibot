from ..commons.bracket import Bracket as commonsBracket
from ..commons.opponent import SoloOpponent
from ..commons.template import Template

class Bracket(commonsBracket):
	def getSoloOpponent(self, template: Template, nameKey: str, scoreKey: str) -> SoloOpponent:
		return SoloOpponent(
			name = template.get(nameKey),
			link = template.get(f'{nameKey}link'),
			flag = template.get(f'{nameKey}flag'),
			race = template.get(f'{nameKey}race'),
			score = template.get(scoreKey)
		)
