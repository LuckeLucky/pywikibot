from typing import Dict

from ..commons.template import Template
from ..commons.bracket import Bracket as commonsBracket
from ..commons.opponent import TeamOpponent

RESET_MATCH = 'RxMBR'
THIRD_PLACE_MATCH = 'RxMTP'

class Bracket(commonsBracket):
	def getTeamOpponent(self, template: Template, nameKey: str, scoreKey: str) -> TeamOpponent:
		mapScores = [x.strip() for x in template.get(scoreKey).split(',')]
		opponentArgs = {
			'name': template.get(nameKey)
		}
		for mapIndex, mapScore in enumerate(mapScores):
			ms = '{{MS|'
			if mapScore == '-':
				break
			ms += mapScore.replace('-', '|')
			opponentArgs[f'm{mapIndex + 1}'] = ms + '}}'

		return TeamOpponent(**opponentArgs)

	def _populateData(self, mapping: Dict[str, Dict[str, str] | str]) -> None:
		for roundParam, _ in mapping.items():
			if roundParam in [RESET_MATCH, THIRD_PLACE_MATCH]:
				continue

			opponents = []
			for i in range(1, 50):
				key = f'p{i}team'
				if not self.getValue(key):
					break
				opponents.append(self.getOpponent(self.template, key, f'p{i}results'))

			match = self.createMatch(opponents, self.template, '')
			match.isValidResetOrThird = False
			self.data[roundParam] = match
