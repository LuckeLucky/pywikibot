r"""
This bot will make direct text replacements.

It will retrieve information on which pages might need changes either from
an XML dump or a text file, or only change a single page.

These command line parameters can be used to specify which pages to work on:

&params;

Furthermore, the following command line parameters are supported:

-isMatchList	Is MatchListTemplate? Showmatch included
-oldTemplateId
-newTemplateId
-bracketType	Only required for brackets

Examples
--------
python pwb.py add_m2_wrapper -lang:valorant -isMatchList -oldTemplateId:"MatchListStart" -newTemplateId:"LegacyMatchListStart" -transcludes:"MatchListStart" -ns:0,2

python pwb.py add_m2_wrapper -lang:valorant -oldTemplateId:"2SETeamBracket" -newTemplateId:"Bracket/2" -bracketType:"team" -ns:0,2 -transcludes:"2SEBracket" -pt:1
"""

import sys
import mwparserfromhell
import pywikibot

from pywikibot import pagegenerators

from scripts.match2.commons.utils import generateId
from scripts.utils import get_text, put_text

def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	isMatchList = False
	oldTemplateId = ''
	newTemplateId = ''
	bracketType = ''

	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, value = arg.partition(':')
			if arg == 'isMatchList':
				isMatchList = True
			if arg == 'oldTemplateId':
				oldTemplateId = value
			if arg == 'newTemplateId':
				newTemplateId = value
			if arg == 'bracketType':
				bracketType = value

	if not oldTemplateId:
		oldTemplateId = pywikibot.input('Old template name:')

	if not newTemplateId:
		newTemplateId = pywikibot.input('New template name:')

	newTemplateText = ''

	if not isMatchList:
		if not bracketType:
			bracketType = pywikibot.input('Type:')

		if bracketType not in ['team', 'solo']:
			pywikibot.stdout("<<lightred>>bracket type error")
			sys.exit(1)

		newTemplateText = f'LegacyBracket|{newTemplateId}|{oldTemplateId}|type={bracketType}|id='
	else:
		newTemplateText = f'{newTemplateId}|id='

	editSummary = f'Convert {oldTemplateId} to Legacy Version'
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		if not page.has_permission():
			continue
		text = get_text(page)
		wikicode = mwparserfromhell.parse(text)
		for template in wikicode.filter_templates():
			if template.name.matches(oldTemplateId):
				templateStr = str(template)
				templateStr = templateStr.replace(oldTemplateId, newTemplateText + generateId(), 1)
				wikicode.replace(template, templateStr)

		newText = str(wikicode)
		if text != newText:
			pywikibot.showDiff(text, newText, context=1)
			put_text(page, summary=editSummary, new=newText)

if __name__ == '__main__':
	main()
