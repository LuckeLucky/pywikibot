import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from match2conversion.bracket import Bracket
from utils import get_text, put_text

def process_text(text: str, templateToReplace: str):
	while(True):
		wikicode = mwparserfromhell.parse(text)
		bracket = None
		for template in wikicode.filter_templates():
			if template.name.matches(templateToReplace):
				bracket = template

		if bracket is None:
			break

		newBracket = Bracket(templateToReplace, bracket)	
		newBracket.process()
		wikicode.replace(bracket, str(newBracket))
		text = str(wikicode)

	return text

def main(*args):

	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	templateToReplace = ''

	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, value = arg.partition(':')
			if arg == 'template':
				templateToReplace = value

	if not templateToReplace:
		templateToReplace = pywikibot.input('Template to replace:')

	if not Bracket.check_support(templateToReplace):
		pywikibot.stdout("<<lightred>>Missing support for template: " + templateToReplace)
		return

	edit_summary = f'Convert Bracket {templateToReplace} to Match2'
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		new_text = process_text(text, templateToReplace)
		#put_text(page, summary=edit_summary, new=new_text)

if __name__ == '__main__':
	main()