from mwparserfromhell.nodes import Template

from ..opponent import Opponent, TeamOpponent
from scripts.match2.opponent import Opponent
from ..bracket import Bracket as Base
from .match import Match

from scripts.utils.parser_helper import get_value

class BracketCounterstrike(Base):
	def __init__(self, oldTemplateName: str, bracket: Template) -> None:
		super().__init__(oldTemplateName, bracket)

	def match_class(self):
		return Match
	
	def get_team_opponent(self, key: str, scoreKey: str) -> Opponent:
		name = get_value(self.bracket, key + 'team')
		csName = get_value(self.bracket, key)
		literal = get_value(self.bracket, key + 'literal')
		score = get_value(self.bracket, key + scoreKey)
		if name is not None:
			return TeamOpponent(name, score)
		elif csName is not None:
			return Opponent(csName, score)
		elif literal is not None:
			return Opponent(literal, score)
		else:
			return None