import pywikibot
import mwparserfromhell

from pywikibot import pagegenerators

from scripts.match2conversion.bracket import Bracket
from utils import get_text, put_text

def process_text(text: str, templateName: str):
	wikicode = mwparserfromhell.parse(text)
	bracket = None
	for template in wikicode.filter_templates():
		if template.name.matches(templateName):
			bracket = template

	if bracket:
		newBracket = Bracket(templateName, bracket)	
		wikicode.replace(bracket, str(newBracket))

	return wikicode

def main(*args):

	# summary message
	edit_summary = 'Converting Brackets to Match2'

	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	templateName = ''

	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, value = arg.partition(':')
			if arg == 'template':
				templateName = value

	if not templateName:
		templateName = pywikibot.input('Template to replace:')

	if not Bracket.check_support(templateName):
		pywikibot.stdout("<<lightred>>Missing support for template: " + templateName)
		return

	generator = genFactory.getCombinedGenerator()

	for page in generator:
		text = get_text(page)
		new_text = process_text(text, templateName)
		put_text(page, summary=edit_summary, new=new_text)

if __name__ == '__main__':
	main()