from mwparserfromhell.nodes import Template

from .commons.bracket import Bracket
from .leagueoflegends.bracket import BracketLeagueOfLegends
from .leagueoflegends.showmatch import ShowmatchLeagueOfLegends

from .counterstrike.bracket import BracketCounterstrike

class BracketFactory:
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
	def getShowmatchClassForLanguage(language: str, template: Template):
		showmatchClass = ShowmatchFactory.mappings[language]
		if showmatchClass:
			return showmatchClass(template)
		else:
			raise ValueError(f"Unsupported language: {language}")