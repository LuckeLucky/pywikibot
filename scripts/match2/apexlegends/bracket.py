import sys
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
			'name': template.get(f'{nameKey}team'),
			'startingpoints': template.get(f'{nameKey}changes')
		}
		for mapIndex, mapScore in enumerate(mapScores):
			ms = '{{MS|'
			if mapScore == '-':
				ms += '|'
			else:
				ms += mapScore.replace('-', '|')
			opponentArgs[f'm{mapIndex + 1}'] = ms + '}}'

		return TeamOpponent(**opponentArgs)

	def _populateData(self, mapping: Dict[str, Dict[str, str] | str]) -> None:
		for roundParam, _ in mapping.items():
			if roundParam in [RESET_MATCH, THIRD_PLACE_MATCH]:
				continue

			opponents = []
			for i in range(1, 50):
				key = f'p{i}'
				if self.getValue(key + 'temp_tie'):
					sys.exit("IDK what is temp tie")
				if not self.getValue(key + 'team'):
					break
				opponents.append(self.getOpponent(self.template, key, f'p{i}results'))

			match = self.createMatch(opponents, self.template, '')
			match.isValidResetOrThird = False
			self.data[roundParam] = match
