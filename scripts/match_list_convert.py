from match2conversion import Match, Opponent, MatchList

import mwparserfromhell
from mwparserfromhell.nodes import Template

import pywikibot
from pywikibot import pagegenerators
from scripts.utils.parser_helper import remove_and_squash
from scripts.utils.text_handler import get_text, put_text

def process_text(text: str):
	while(True):
		wikicode = mwparserfromhell.parse(text)

		previousTemplate = None
		matchListStart = None
		matchMaps = []
		matchListEnd = None

		for template in wikicode.filter_templates():
			if template.name.matches('MatchListStart'):
				matchListStart = template
				if previousTemplate.name.matches('GroupTableLeague'):
						template.add('attached', 'true')

			if template.name.matches('MatchMaps'):
				matchMaps.append(template)

			if template.name.matches('MatchListEnd'):
				matchListEnd = template
				break

			previousTemplate = template

		if matchListEnd is None:
			break

		matchList = MatchList(matchListStart, matchMaps)
		matchList.process()
		wikicode.replace(matchListStart, str(matchList))

		#Remove old templates
		for matchMap in matchMaps:
			remove_and_squash(wikicode, matchMap)
		remove_and_squash(wikicode, matchListEnd)

		text = str(wikicode)

	return text

def main(*args):

	# summary message
	edit_summary = 'Converting MatchLists to Match2'

	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue

	generator = genFactory.getCombinedGenerator()

	for page in generator:
		text = get_text(page)
		new_text = process_text(text)
		put_text(page, summary=edit_summary, new=new_text)

if __name__ == '__main__':
	main()