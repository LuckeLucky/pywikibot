from typing import Literal
from .templateutils import TemplateUtils
from .template import Template
from .opponent import Opponent, SoloOpponent, TeamOpponent

class MatchGroup(TemplateUtils):
	def __init__(self, template):
		super().__init__(template)
		self.matchGroupType: Literal["solo", "team"] = self.template.get('type')

	def getSoloOpponent(self, template: Template, nameKey: str, scoreKey: str) -> SoloOpponent:
		return SoloOpponent(
			name = template.get(nameKey),
			link = template.get(f'{nameKey}link'),
			flag = template.get(f'{nameKey}flag'),
			score = template.get(scoreKey)
		)

	def getTeamOpponent(self, template: Template, nameKey: str, scoreKey: str) -> TeamOpponent:
		return TeamOpponent(
			name = template.getfirstValueFound([f'{nameKey}team', nameKey]),
			score = template.get(scoreKey)
		)

	def getOpponent(self, template: Template, nameKey: str, scoreKey: str) -> Opponent:
		opponentGet = getattr(self, 'get' + self.matchGroupType.capitalize() + 'Opponent')
		if not opponentGet:
			raise ValueError(f'{self.matchGroupType} is not supported')
		return opponentGet(template, nameKey, scoreKey)