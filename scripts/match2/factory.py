from mwparserfromhell.nodes import Template

from .commons.bracket import Bracket
from .leagueoflegends.bracket import BracketLeagueOfLegends
from .counterstrike.bracket import BracketCounterstrike

from .commons.showmatch import Showmatch
from .leagueoflegends.showmatch import ShowmatchLeagueOfLegends
from .wildrift.showmatch import ShowmatchWildRift

from .commons.matchlist import Matchlist
from .leagueoflegends.matchlist import MatchlistLeagueOfLegends

bracketMappings = {
	'leagueoflegends': BracketLeagueOfLegends,
	'counterstrike': BracketCounterstrike
}

def getBracketClassForLanguage(language: str):
	bracketClass = bracketMappings[language]
	if bracketClass:
		return bracketClass
	return Bracket

showmatchMappings = {
	'leagueoflegends': ShowmatchLeagueOfLegends,
	'wildrift': ShowmatchWildRift
}

def getShowmatchClassForLanguage(language: str, template: Template):
	showmatchClass = showmatchMappings[language]
	if showmatchClass:
		return showmatchClass(template)
	return Showmatch

matchlistMappings = {
	'leagueoflegends': MatchlistLeagueOfLegends
}

def getMatchlistClassForLanguage(language: str) -> Matchlist:
	matchlistClass = matchlistMappings[language]
	if matchlistClass:
		return matchlistClass
	return Matchlist