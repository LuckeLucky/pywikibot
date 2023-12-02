from mwparserfromhell.nodes import Template

from ..commons.utils import *
from ..commons.opponent import Opponent, TeamOpponent
from ..commons.bracket import Bracket
from .match import Match

class BracketCounterstrike(Bracket):
	def __init__(self, oldTemplateName: str, bracket: Template) -> None:
		super().__init__(oldTemplateName, bracket)

	def match_class(self):
		return Match
	
	def get_team_opponent(self, key: str, scoreKey: str) -> Opponent:
		name = get_parameter_str(self.bracket, key + 'team')
		csName = get_parameter_str(self.bracket, key)
		literal = get_parameter_str(self.bracket, key + 'literal')
		score = get_parameter_str(self.bracket, key + scoreKey)
		if name is not None:
			return TeamOpponent(name, score)
		elif csName is not None:
			return Opponent(csName, score)
		elif literal is not None:
			return Opponent(literal, score)
		else:
			return None