from mwparserfromhell.nodes import Template

from .commons.bracket import Bracket
from .leagueoflegends.bracket import BracketLeagueOfLegends
from .counterstrike.bracket import BracketCounterstrike
from .wildrift.bracket import BracketWildRift
from .valorant.bracket import BracketValorant

from .commons.showmatch import Showmatch
from .leagueoflegends.showmatch import ShowmatchLeagueOfLegends
from .wildrift.showmatch import ShowmatchWildRift

from .commons.matchlist import Matchlist
from .leagueoflegends.matchlist import MatchlistLeagueOfLegends
from .wildrift.matchlist import MatchlistWildRift
from .counterstrike.matchlist import MatchlistCounterStrike
from .valorant.matchlist import MatchlistValorant

bracketMappings = {
	'leagueoflegends': BracketLeagueOfLegends,
	'wildrift': BracketWildRift,
	'counterstrike': BracketCounterstrike,
	'valorant': BracketValorant
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
	'leagueoflegends': MatchlistLeagueOfLegends,
	'wildrift': MatchlistWildRift,
	'counterstrike': MatchlistCounterStrike,
	'valorant': MatchlistValorant
}

def getMatchlistClassForLanguage(language: str) -> Matchlist:
	matchlistClass = matchlistMappings[language]
	if matchlistClass:
		return matchlistClass
	return Matchlist