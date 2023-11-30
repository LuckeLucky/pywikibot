from mwparserfromhell.nodes import Template
from .leagueoflegends.bracket import BracketLeagueOfLegends

class BracketFactory(object):
	mappings = {
		'leagueoflegends': BracketLeagueOfLegends
	}
	@staticmethod
	def new_bracket(language: str, old_template_name: str, bracket: Template):
		bracket_class = BracketFactory.mappings[language]
		if bracket_class:
			return bracket_class(old_template_name, bracket)
		else:
			raise ValueError(f"Unsupported language: {language}")