import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from match2conversion import MatchList
from scripts.match2conversion.match_list import MatchListLegacy
from scripts.utils.parser_helper import remove_and_squash
from scripts.utils.text_handler import get_text, put_text

def process(text: str):
	while(True):
		wikicode = mwparserfromhell.parse(text)

		previousTemplate = None
		matchListStart = None
		matchMaps = []
		matchListEnd = None

		for template in wikicode.filter_templates():
			if template.name.matches('MatchListStart'):
				matchListStart = template
				if (previousTemplate.name.matches('GroupTableLeague')
					or previousTemplate.name.matches('GroupTableEnd')):
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

def process_legacy(text: str):
	while(True):
		wikicode = mwparserfromhell.parse(text)

		previousTemplate = None
		matchList = None

		for template in wikicode.filter_templates():
			if template.name.matches('MatchList'):
				matchList = template
				if (previousTemplate.name.matches('GroupTableLeague')
					or previousTemplate.name.matches('GroupTableEnd')):
					template.add('attached', 'true')
				break

			previousTemplate = template

		if matchList is None:
			break

		newMatchList = MatchListLegacy(matchList)
		newMatchList.process()
		wikicode.replace(matchList, str(newMatchList))

		text = str(wikicode)

	return text


def process_text(text: str, legacy: bool = False):
	return process(text) if not legacy else process_legacy(text)

def main(*args):

	# summary message
	edit_summary = 'Convert MatchLists to Match2'

	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()
	isLegacy = False

	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			if arg == '-legacy':
				isLegacy = True

	generator = genFactory.getCombinedGenerator()

	for page in generator:
		text = get_text(page)
		new_text = process_text(text, isLegacy)
		put_text(page, summary=edit_summary, new=new_text)

if __name__ == '__main__':
	main()