from typing import List, Dict

import mwparserfromhell

import pywikibot
from pywikibot import pagegenerators
from scripts.match2.commons.utils import generateId
from scripts.match2.commons.template import Template
from scripts.match2.commons.matchlist import Matchlist
from scripts.match2.factory import getMatchlistClassForLanguage
from scripts.utils import get_text, put_text, remove_and_squash

def processText(matchlistClass: Matchlist, text: str, config: Dict[str, str]) -> str:
	startName = config['matchStart'] if 'matchStart' in config else 'LegacyMatchListStart'
	matchName = config['match'] if 'match' in config else 'MatchMaps'
	endName = config['matchEnd'] if 'matchEnd' in config else 'MatchListEnd'
	while True:
		matchlist: Template = None
		matchListStart: Template = None
		matchMaps: List[Template] = []
		templatesToRemove: List[Template] = []
		ends = False

		wikicode = mwparserfromhell.parse(text)
		for template in wikicode.filter_templates():
			if template.name.matches(startName):
				matchListStart = template
				matchMaps = []
				templatesToRemove = []
			if template.name.matches(matchName):
				matchMaps.append(Template(template))
				templatesToRemove.append(template)
			if template.name.matches(endName):
				templatesToRemove.append(template)
				ends = True
				break

		if not ends:
			break

		matchlist = Template(matchListStart)
		matchlist.addIfNotHas('id', generateId())

		ml = matchlistClass(matchlist, matchMaps)
		wikicode.replace(matchListStart, str(ml))
		for template in templatesToRemove:
			remove_and_squash(wikicode, template)

		text = str(wikicode)

	return text

def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()
	save = True
	isLegacy = False
	config: Dict[str, str] = {
		'matchStartId': '',
		'matchMapsId': '',
		'matchEndId': ''
	}

	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, _ = arg.partition(':')
			if arg == 'nosave':
				save = False
			if arg == '-legacy':
				isLegacy = True

	

	matchlistClass: Matchlist = getMatchlistClassForLanguage(genFactory.site.code)

	editSummary = 'Convert Matchlist to Match2'
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = processText(matchlistClass, text, config)
		if save:
			put_text(page, summary=editSummary, new=newText)
		else:
			print(newText)

if __name__ == '__main__':
	main()
