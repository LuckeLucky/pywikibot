import json
from pathlib import Path

from ..commons.utils import getStringFromTemplate
from ..commons.opponent import Opponent, TeamOpponent
from ..commons.bracket import Bracket
from .match import Match

class BracketCounterstrike(Bracket):
	Match = Match

	@classmethod
	def loadCustomMapping(cls):
		filePath = Path(__file__).with_name('bracket_custom_mappings.json')
		with filePath.open(encoding='utf-8') as file:
			data = json.load(file)
			cls.customMapping = data

	def getTeamOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = getStringFromTemplate(self.template, key + 'team')
		score = getStringFromTemplate(self.template, key + scoreKey)
		if name:
			return TeamOpponent(name, score)
		csName = getStringFromTemplate(self.template, key)
		if csName:
			return Opponent(csName, score)
		return TeamOpponent()
