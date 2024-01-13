import json
from pathlib import Path

from ..commons.opponent import Opponent, TeamOpponent
from ..commons.bracket import Bracket
from .match import Match

class BracketValorant(Bracket):
	Match = Match

	@classmethod
	def loadCustomMapping(cls):
		filePath = Path(__file__).with_name('bracket_custom_mappings.json')
		with filePath.open(encoding='utf-8') as file:
			data = json.load(file)
			cls.customMapping = data

	def getTeamOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.template.getValue(key + 'team')
		score = self.template.getValue(key + scoreKey)
		if name:
			return TeamOpponent(name, score)
		return TeamOpponent()