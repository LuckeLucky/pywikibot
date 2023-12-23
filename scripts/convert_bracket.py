import sys
import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from scripts.match2.factory import getBracketClassForLanguage
from scripts.match2.commons.template import Template
from scripts.utils import get_text, put_text

def processText(bracketClass, text: str):
	while True:
		wikicode = mwparserfromhell.parse(text)
		legacyBracket = None
		for template in wikicode.filter_templates():
			if template.name.matches('LegacyBracket'):
				legacyBracket = template
				break

		if legacyBracket is None:
			break
		newBracket = bracketClass(Template(legacyBracket, removeComments=True))
		if not bracketClass.isBracketDataAvailable(newBracket.newTemplateId):
			pywikibot.stdout("<<lightred>>Missing support for template " + newBracket.newTemplateId)
			sys.exit(1)
		newBracket.process()
		wikicode.replace(legacyBracket, str(newBracket))

		text = str(wikicode)

	return text

def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	save = True

	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, _ = arg.partition(':')
			if arg == 'nosave':
				save = False

	language = genFactory.site.code
	if not language:
		return

	bracketClass = getBracketClassForLanguage(language)

	editSummary = 'Convert LegacyBracket to Match2'
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = processText(bracketClass, text)
		if save:
			put_text(page, summary=editSummary, new=newText)
		else:
			print(newText)

if __name__ == '__main__':
	main()
