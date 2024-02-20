from typing import List
from scripts.match2.commons.opponent import Opponent, TeamOpponent
from scripts.match2.commons.template import Template

from ..commons.matchlist import Matchlist as commonsMatchlist

class Matchlist(commonsMatchlist):
	def __init__(self, template: Template, matchTemplates: List[Template]):
		super().__init__(template, matchTemplates)
		self.args['matchsection'] = self.template.getValue('matchsection')

	def getTeamOpponent(self, template: Template, key: str, scoreKey: str) -> Opponent:
		name = template.getValue(key)
		score = template.getValue(scoreKey)
		if name:
			return TeamOpponent(name, score)
		name = template.getfirstValueFound([
			key + 'cstrike',
			key + 'css',
			key + 'csgo'
		])
		if name:
			return Opponent(name, score)
		return TeamOpponent()
