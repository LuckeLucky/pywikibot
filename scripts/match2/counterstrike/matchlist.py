from typing import List
from scripts.match2.commons.opponent import Opponent, TeamOpponent
from scripts.match2.commons.template import Template

from ..commons.matchlist import Matchlist as commonsMatchlist

class Matchlist(commonsMatchlist):
	def __init__(self, template: Template, matchTemplates: List[Template]):
		super().__init__(template, matchTemplates)
		self.args['matchsection'] = self.getValue('matchsection')

	def getTeamOpponent(self, template: Template, nameKey: str, scoreKey: str) -> Opponent:
		name = template.getValue(nameKey)
		score = template.getValue(scoreKey)
		if name:
			return TeamOpponent(name = name, score = score)
		name = template.getfirstValueFound([
			nameKey + 'cstrike',
			nameKey + 'css',
			nameKey + 'csgo'
		])
		if name:
			return Opponent(name = name, score = score)
		return TeamOpponent()
