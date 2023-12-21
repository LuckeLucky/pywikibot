from typing import List

import mwparserfromhell
from mwparserfromhell.nodes import Template

import pywikibot
from pywikibot import pagegenerators
from scripts.match2.commons.matchlist import Matchlist
from scripts.match2.factory import getMatchlistClassForLanguage
from scripts.utils import get_text, put_text, remove_and_squash


def processTextLegacy(matchlistClass: Matchlist, text: str) -> str:
	#TODO
	return text

def processText(matchlistClass: Matchlist, text: str) -> str:
	while True:
		matchListStart: Template = None
		matchMaps: List[Template] = []
		templatesToRemove: List[Template] = []
		ends = False

		wikicode = mwparserfromhell.parse(text)
		for template in wikicode.filter_templates():
			if template.name.matches('LegacyMatchListStart'):
				matchListStart = template
				matchMaps = []
				templatesToRemove = []
			if template.name.matches('MatchMapsLua'):
				matchMaps.append(template)
				templatesToRemove.append(template)
			if template.name.matches('MatchListEnd'):
				templatesToRemove.append(template)
				ends = True
				break

		if not ends:
			break

		matchList = matchlistClass(matchListStart, matchMaps)
		matchList.process()
		wikicode.replace(matchListStart, str(matchList))
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
		if isLegacy:
			newText = processTextLegacy(matchlistClass, text)
		else:
			newText = processText(matchlistClass, text)
		if save:
			put_text(page, summary=editSummary, new=newText)
		else:
			print(newText)

if __name__ == '__main__':
	main()
