import json
from pathlib import Path

from ..commons.bracket import Bracket
from .match import Match
from ..commons.utils import getStringFromTemplate
from ..commons.opponent import Opponent, TeamOpponent

class BracketLeagueOfLegends(Bracket):
	Match = Match
	bracketAlias = {
		'DemaciaCupTeamBracket': '8L8D-4Q-4L4D-2Q-2L2D-1Q',
		'NESTTeamBracket': '2L2DH2L-1Q',
		'8STeamBracket': '2L6D',
		'8Qual-8SE4DETeamBracket': '8L4D-4Q-U-8-4Q',
		'7STeamBracket': '2L5D',
		'1Qual-2SE1LTeamBracket': '2U2-1Q',
		'2Qual-4STeamBracket': '2L2D-2QL',
		'32SE4STeamBracket': '32L4DSS',
		'3Qual-5DETeamBracketSpecial': '2L1D-1Q-2-1Q-U-2-1Q',
		'4Qual-12DE4STeamBracket': '8L4DS-2Q-U-8L4DSL2D-2Q',
		'4SE6STeamBracket': '4L6DS',
		'4TeamBracketSpecial': '2L2D',
		'5Qual-16DETeamBracket': '16-2Q-U-8L4DSL2D-2Q-2-1Q',
		'6Qual-12SETeamBracket': '8-4Q-4-2Q',
		'9SETeamBracket': '2L1DH2LH4L',
		'6STeamBracket': '2L4D',
		'12DE4STeamBracket2': '8L4DSSU8L2DSL1D',
		'12DETeamBracket': '8L4DSSU8L2DSL1D',
		'1Qual-6SETeamBracket': '4L2DS-1Q',
		'3Qual-5DETeamBracket': '2-1Q-U-4-1Q-U-2L1D-1Q',
		'32DETeamBracket': '32U16L8DSL4DSL2DSL1D',
	}
	bracketAlias.update(Bracket.bracketAlias)

	@classmethod
	def loadCustomMapping(cls):
		filePath = Path(__file__).with_name('bracket_custom_mappings.json')
		with filePath.open(encoding='utf-8') as file:
			data = json.load(file)
			cls.customMapping = data

	def getTeamOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = getStringFromTemplate(self.template, key + 'team')
		score = getStringFromTemplate(self.template, key + scoreKey)
		if name is not None:
			return TeamOpponent(name, score)
		leagueName = getStringFromTemplate(self.template, key + 'league')
		if leagueName is not None:
			return Opponent(leagueName, score)
		leagueName = getStringFromTemplate(self.template, key)
		if leagueName is not None:
			return Opponent(leagueName, score)
		literal = getStringFromTemplate(self.template, key + 'literal')
		if literal is not None:
			return Opponent(literal, score)
		return None
