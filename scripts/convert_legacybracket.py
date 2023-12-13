import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from match2.factory import BracketFactory
from match2.commons.utils import get_parameter_str
from utils import get_text, put_text, remove_and_squash

def processText(bracketClass, text: str):
	while(True):
		wikicode = mwparserfromhell.parse(text)
		legacyBracket = None
		for template in wikicode.filter_templates():
			if template.name.matches('LegacyBracket'):
				legacyBracket = template
				break

		if legacyBracket is None:
			break
		newBracket = bracketClass.createNewBracket(legacyBracket)
		if not bracketClass.isBracketDataAvailable(newBracket.newTemplateId):
			pywikibot.stdout("<<lightred>>Missing support for template " + newBracket.newTemplateId)
			exit(1)
		newBracket.process()
		wikicode.replace(legacyBracket, str(newBracket))

		text = str(wikicode)

	return text

def main(*args):
	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	save = True

	for arg in local_args:
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

	bracketClass = BracketFactory.getBracketClassForLanguage(language)

	edit_summary = f'Convert LegacyBracket to Match2'
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = processText(bracketClass, text)
		if save:
			put_text(page, summary=edit_summary, new=newText)
		else:
			print(newText)

if __name__ == '__main__':
	main()