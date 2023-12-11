from mwparserfromhell.nodes import Template

from .commons.bracket import Bracket
from .leagueoflegends.bracket import BracketLeagueOfLegends
from .leagueoflegends.showmatch import ShowmatchLeagueOfLegends

from .counterstrike.bracket import BracketCounterstrike

class BracketFactory(object):
	mappings = {
		'leagueoflegends': BracketLeagueOfLegends,
		'counterstrike': BracketCounterstrike
	}
	@staticmethod
	def getBracketClassForLanguage(language: str):
		bracketClass = BracketFactory.mappings[language]
		if bracketClass:
			return bracketClass
		else:
			return Bracket
		
class ShowmatchFactory(object):
	mappings = {
		'leagueoflegends': ShowmatchLeagueOfLegends
	}
	@staticmethod
	def new_showmatch(language: str, template: Template):
		showmatch_class = ShowmatchFactory.mappings[language]
		if showmatch_class:
			return showmatch_class(template)
		else:
			raise ValueError(f"Unsupported language: {language}")