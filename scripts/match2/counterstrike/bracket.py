from mwparserfromhell.nodes import Template
import json
from pathlib import Path

from ..commons.utils import *
from ..commons.opponent import Opponent, TeamOpponent
from ..commons.bracket import Bracket
from .match import Match

class BracketCounterstrike(Bracket):
	Match = Match
	bracketAlias = {
		'2SETeamBracket/compact': '2',
		'8SETeamBracket/reseeded': '8',
		'16SETeamBracket/css': '16',
		'4DETeamBracket': '4U2L1D',
		'8DETeamBracket': '8U4L2DSL1D',
		'8DEBracket': '8U4L2DSL1D',
		'16DETeamBracket': '16U8L4DSL2DSL1D',
		'32DETeamBracket': '32U16L8DSL4DSL2DSL1D',
		'1DE2STeamBracket': '2U2',
		'2DE1STeamBracket': '2U2',
		'2DE1WTeamBracket': '2L1DU2',
		'2DE2STeamBracket': '2U2L1D',
		'2DE4STeamBracket': '2U4L1D',
		'3SETeamBracket': '2L1D',
		'4DE1STeamBracket2': '4L2DSU2L2D',
		'4DE2S2STeamBracket': '4L4DSU4L2DSL1D',
		'4DE2STeamBracket': '4U4L1D',
		'4DE2WTeamBracket': '4L2DSU4L1D',
		'4DE4STeamBracket': '4U4L2DSL1D',
		'4DE8STeamBracket': '4U8L2DSL1D',
		'4LTeamBracket': '4L2DSL1D',
		'4SE-ChampTeamBracket': '4L1D',
		'4SE4STeamBracket': '4L4DS',
		'4SE6STeamBracket': '4L6DS',
		'4SEKoTHTeamBracket': '2L2D',
		'4STeamBracket': '2L2D',
		'5KoTHTeamBracket': '2L3D',
		'5SEKoTHTeamBracket': '2L3D',
		'6DE4LTeamBracket': '4L2DSU4L4DSL1D',
		'6SETeamBracket': '4L2DS',
		'8DE2STeamBracket': '8L2DSU4L4DSL1D',
		'8DE4LTeamBracket': '8U8L2DSL1D',
		'8DE8STeamBracket': '8U8L4DSL2DSL1D',
		'8DE8STeamBracket2': '16U4L2DSL1D',
		'8DETeamGroupBracket': '8-U-4L2DS',
		'8LTeamBracket': '8L4DSL2DSL1D',
		'8SE2S2STeamBracket': '8L4DS',
		'8SE2STeamBracket': '8L2DS',
		'8SE4DETeamBracket': '8U2L1D',
		'8SE4S4S2STeamBracket': '8L8DSL2DS',
		'8SE4S4STeamBracket': '8L8DSS',
		'8SE4STeamBracket': '8L4DSS',
		'8SEMixedTeamBracket': '4H4L2DLS',
		'12DE4STeamBracket': '8L4DSSU8L4DSL2DSL1D',
		'12DETeamBracket': '8L4DSSU8L2DSL1D',
		'16DE8LTeamBracket': '16U16L4DSL2DSL1D',
		'16DE8STeamBracket': '16L8DSSSU16L4DSL2DSL1D',
		'16LTeamBracket': '8L4DSL2DSL1D-8L4DSL2DSL1D',
		'16SE2STeamBracket': '16L2DS',
		'16SE4STeamBracket2': '8L4DSSH8L',
		'16SE8STeamBracket': '16L8DSSS',
		'32DE16STeamBracket': '32L16DSSSSU32L8DSL4DSL2DSL1D',
		'32SE2STeamBracket': '32L2DS',
		'32SE8STeamBracket': '32L8DSSS',
		'1Qual-16SETeamBracket': '16-1Q',
		'1Qual-2LTeamBracket': '2L1D-1Q',
		'1Qual-2SETeamBracket': '2-1Q',
		'1Qual-4DETeamBracket': '4U2L1D-1Q',
		'1Qual-4SETeamBracket': '4-1Q',
		'1Qual-8SETeamBracket': '8-1Q',
		'2Qual-16DETeamBracket': '16-1Q-U-8L4DSL2DSL1D-1Q',
		'2Qual-16SE2STeamBracket': '16L2D-2Q',
		'2Qual-16SE8S4DETeamBracket': '16L8DSSS-1Q-U-2L1D-1Q',
		'2Qual-2DE1LTeamBracket': '2-1Q-U-2-1Q',
		'2Qual-2DE2STeamBracket': '2-1Q-U-2L1D-1Q',
		'2Qual-2DE4STeamBracket': '2-1Q-U-4L1D-1Q',
		'2Qual-4SETeamBracket': '4-2Q',
		'2Qual-4SETeamBracket/noqual': '2-2',
		'2Qual-4SETeamBracket2': '4-2QL',
		'2Qual-8SETeamBracket': '8-2Q',
		'2Qual-16SETeamBracket': '16-2Q',
		'2Qual-32DETeamBracket': '32-1Q-U-16L8DSL4DSL2DSL1D-1Q',
		'2Qual-32SETeamBracket': '32-2Q',
		'2Qual-4DE1STeamBracket': '4L2DS-1Q-U-2L2D-1Q',
		'2Qual-4DE2WTeamBracket': '4L2DS-1Q-U-4L1D-1Q',
		'2Qual-4DE4STeamBracket': '4-1Q-U-4L2DSL1D-1Q',
		'2Qual-4DETeamBracket': '4-1Q-U-2L1D-1Q',
		'2Qual-4DETeamBracket/noqual': '4-U-2L1D',
		'2Qual-4SE2S2S2STeamBracket': '4L6D-2Q',
		'2Qual-4SE2S2STeamBracket': '4L4D-2Q',
		'2Qual-4SE4STeamBracket': '4L4D-2Q',
		'2Qual-64SETeamBracket': '64-2Q',
		'2Qual-6SETeamBracket': '4L2D-2Q',
		'2Qual-8DETeamBracket': '8-1Q-U-4L2DSL1D-1Q',
		'2Qual-8SE2STeamBracket': '8L2D-2Q',
		'2Qual-8SE4STeamBracket': '8L4DS-2Q',
		'3NQual-4SETeamBracket': '2-2-U-2',
		'3Qual-12SETeamBracket': '8-2Q-4-1Q',
		'3Qual-16DETeamBracket': '16-2Q-U-8L4DSL2DS-1Q',
		'3Qual-16SETeamBracket': '16-2Q-2-1Q',
		'3Qual-32SETeamBracket': '32-2Q-2-1Q',
		'3Qual-4DE2WTeamBracket': '4L2D-2Q-U-4-1Q',
		'3Qual-4DETeamBracket': '4-2Q-U-2-1Q',
		'3Qual-4SETeamBracket': '4-2Q-U-2-1Q', #3rd place match need mapping
		'3Qual-6SE3S3STeamBracket/noqual': '2L2D-2L2D-2L2D',
		'3Qual-6SETeamBracket': '4L2D-2Q-2-1Q',
		'3Qual-6SETeamBracket2': '4-2Q-2-1Q',
		'3Qual-8DE4STeamBracket': '8L4DS-2Q-U-8L2DS-1Q',
		'3Qual-8DE4STeamBracket2': '8L4DS-2Q-U-4L2DS-1Q',
		'3Qual-8DETeamBracket': '8-2Q-U-4L2DS-1Q',
		'3Qual-8DETeamBracket2': '8-2QL-U-4L2DS-1Q',
		'3Qual-8SETeamBracket': '8-2Q-2-1Q',
		'5Qual-16DETeamBracket2': '16-2QL-U-8L4DSL2DS-2QL-U-2-1Q',
		'4Qual-16DETeamBracket': '16-2Q-U-8L4DSL2D-2Q',
		'4Qual-16SETeamBracket': '16-4Q',
		'4Qual-32DETeamBracket': '32-2Q-U-16L8DSL4DSL2D-2Q',
		'4Qual-32SETeamBracket': '32-4Q',
		'4Qual-8DETeamBracket': '8-2Q-U-4L2D-2Q',
		'4Qual-8DETeamBracket2': '8-1Q-U-4L2DSL1D-2QL',
		'4Qual-8SETeamBracket': '8-4Q',
		'4Qual-4DE2STeamBracket': '4-2Q-U-4-2Q',
		'4Qual-4DE4STeamBracket': '4-2Q-U-4L2D-2Q',
		'4Qual-64SETeamBracket': '64-4Q',
		'4Qual-8DE2STeamBracket': '8L2D-2Q-U-4L4D-2Q',
		'4Qual-8DE4LTeamBracket': '8-2Q-U-8L2D-2Q',
		'4Qual-8DE4STeamBracket': '8L4DS-2Q-U-8L2D-2Q',
		'4Qual-8SE4STeamBracket': '8L4D-4Q',
		'5Qual-8DE4STeamBracket': '8L4D-4Q-U-8-1Q',
		'5Qual-8DETeamBracket': '8-4Q-U-4-1Q',
		'5Qual-8DETeamBracket2': '8-2Q-U-4L2D-2Q-2-1Q',
		'6Qual-12SETeamBracket': '8-4Q-4-2Q',
		'6Qual-16DETeamBracket': '16-4Q-U-8L4DS-2Q',
		'6Qual-8DE4STeamBracket': '8L4D-4Q-U-8-2Q',
		'6Qual-8DETeamBracket': '8-4Q-U-4-2Q',
		'8Qual-16DE8LTeamBracket': '16-4Q-U-16L4D-4Q',
		'8Qual-16DETeamBracket': '16-4Q-U-8L4D-4Q',
		'8Qual-16SETeamBracket': '16-8Q',
		'8Qual-32DE4LTeamBracket': '32-4Q-U-16L8DSL8D-4Q',
		'8Qual-32DETeamBracket': '32-4Q-U-16L8DSL4D-4Q',
		'8Qual-32SETeamBracket': '32-8Q',
		'8Qual-64SETeamBracket': '64-8Q',
		'12Qual-16DETeamBracket': '2-2-2-2-2-2-2-2-U-2-2-2-2',
		'16Qual-32DETeamBracket' : '32-8Q-U-16L8D-8Q',
		'16Qual-32SETeamBracket' : '32-16Q',
		'16Qual-64SETeamBracket': '64-16Q',
		'32SE-4RTeamBracket': '32-4Q',
		'4DE2WTeamBracket2': '4L2DSU2L1D',
		'3Qual-8SE4STeamBracket': '8L4DS-2Q-2-1Q',
		'32DETeamBracketCPL' : '32U8L1D',
	}
	bracketAlias.update(Bracket.bracketAlias)

	@classmethod
	def loadCustomMapping(cls):
		p = Path(__file__).with_name('bracket_custom_mappings.json')
		file = p.open()
		data = json.load(file)
		cls.customMapping = data

	def __init__(self, oldTemplateName: str, bracket: Template) -> None:
		super().__init__(oldTemplateName, bracket)
	
	def getTeamOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = get_parameter_str(self.template, key + 'team')
		csName = get_parameter_str(self.template, key)
		literal = get_parameter_str(self.template, key + 'literal')
		score = get_parameter_str(self.template, key + scoreKey)
		if name is not None:
			return TeamOpponent(name, score)
		elif csName is not None:
			return Opponent(csName, score)
		elif literal is not None:
			return Opponent(literal, score)
		else:
			return None