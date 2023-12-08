from mwparserfromhell.nodes import Template

from .leagueoflegends.bracket import BracketLeagueOfLegends
from .leagueoflegends.showmatch import ShowmatchLeagueOfLegends

from .counterstrike.bracket import BracketCounterstrike

class BracketFactory(object):
	mappings = {
		'leagueoflegends': BracketLeagueOfLegends,
		'counterstrike': BracketCounterstrike
	}
	@staticmethod
	def new_bracket(language: str, old_template_name: str, template: Template):
		bracket_class = BracketFactory.mappings[language]
		if bracket_class:
			return bracket_class(old_template_name, template)
		else:
			raise ValueError(f"Unsupported language: {language}")
		
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