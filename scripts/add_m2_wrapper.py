r"""
This bot will make direct text replacements.

It will retrieve information on which pages might need changes either from
an XML dump or a text file, or only change a single page.

These command line parameters can be used to specify which pages to work on:

Examples
--------
python pwb.py add_m2_wrapper -lang:valorant -transcludes:"MatchListStart" -newTemplateId:"LegacyMatchListStart|id=" -ns:0,2

python pwb.py add_m2_wrapper -lang:valorant -transcludes:"8SEBracket" -newTemplateId:"LegacyBracket|Bracket/8|8SEBracket|type=solo|id=" -ns:0,2
"""

import mwparserfromhell
import pywikibot

from pywikibot import pagegenerators

from scripts.match2.commons.utils import generateId
from scripts.utils import get_text, put_text

def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	oldTemplateId = ''
	newTemplateId = ''

	for arg in localArgs:
		if arg.startswith('-'):
			insideArg = arg[1:]
			insideArg, _, value = insideArg.partition(':')
			if insideArg == 'oldTemplateId' or insideArg == 'transcludes':
				oldTemplateId = value
			if insideArg == 'newTemplateId':
				newTemplateId = value
		if genFactory.handle_arg(arg):
			continue

	if not oldTemplateId:
		oldTemplateId = pywikibot.input('Old template name:')

	if not newTemplateId:
		newTemplateId = pywikibot.input('New template name:')

	editSummary = f'Convert {oldTemplateId} to Legacy Version'
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		if not page.has_permission():
			continue
		text = get_text(page)
		wikicode = mwparserfromhell.parse(text)
		for template in wikicode.filter_templates(matches=lambda t : t.name.matches(oldTemplateId)):
			if template.name.matches(oldTemplateId):
				templateStr = str(template)
				templateStr = templateStr.replace(oldTemplateId, newTemplateId + generateId(), 1)
				wikicode.replace(template, templateStr)

		newText = str(wikicode)
		if text != newText:
			pywikibot.showDiff(text, newText, context=1)
			put_text(page, summary=editSummary, new=newText)
		else:
			pywikibot.info(f'No changes were needed on {page}')

if __name__ == '__main__':
	main()
