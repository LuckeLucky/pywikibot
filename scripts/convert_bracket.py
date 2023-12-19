import sys
import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from scripts.match2.factory import getBracketClassForLanguage
from scripts.match2.commons.utils import getStringFromTemplate
from scripts.match2.commons.bracket import Bracket
from scripts.utils import get_text, put_text, remove_and_squash

def processText(bracketClass: Bracket, text: str, oldTemplateId: str):
	shortNames = ''
	while True:
		templatesToRemove = []
		wikicode = mwparserfromhell.parse(text)
		bracketTemplate = None
		for template in wikicode.filter_templates():
			templateName = str(template.name).strip()
			if template.name.matches(oldTemplateId):
				bracketTemplate = template
				if shortNames:
					bracketTemplate.add('shortNames', shortNames)
			if templateName == '#vardefine:bracket_short_teams':
				shortNames = getStringFromTemplate(template, index = 0)
				templatesToRemove.append(template)

		if bracketTemplate is None:
			break
		newBracket = bracketClass.createNewBracket(bracketTemplate, oldTemplateId)
		newBracket.process()
		wikicode.replace(bracketTemplate, str(newBracket))

		for template in templatesToRemove:
			remove_and_squash(wikicode, template)

		text = str(wikicode)

	return text

def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	oldTemplateId = ''
	save = True

	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, value = arg.partition(':')
			if arg == 'template':
				oldTemplateId = value
			if arg == 'nosave':
				save = False

	language = genFactory.site.code
	if not language:
		return

	if not oldTemplateId:
		oldTemplateId = pywikibot.input('Template to replace:')

	bracketClass: Bracket = getBracketClassForLanguage(language)

	if not bracketClass.isAliasSet(oldTemplateId):
		pywikibot.stdout("<<lightred>>Missing support for template: " + oldTemplateId)
		sys.exit(1)

	editSummary = f'Convert Bracket {oldTemplateId} to Match2'
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = processText(bracketClass, text, oldTemplateId)
		if save:
			put_text(page, summary=editSummary, new=newText)
		else:
			print(newText)

if __name__ == '__main__':
	main()
