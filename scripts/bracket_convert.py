import logging
import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from match2conversion.bracket import Bracket
from scripts.match2conversion import match2exceptions
from scripts.match2conversion.bracket_helper import BracketHelper
from scripts.utils.parser_helper import get_value, remove_and_squash
from utils import get_text, put_text

def process_text(text: str, templateToReplace: str):
	shortNames = ''
	while(True):
		templatesToRemove = []
		wikicode = mwparserfromhell.parse(text)
		bracket = None
		for template in wikicode.filter_templates():
			templateName = str(template.name).strip()
			if template.name.matches(templateToReplace):
				bracket = template
				if shortNames:
					bracket.add('shortNames', shortNames)
			if templateName == '#vardefine:bracket_short_teams':
				shortNames = get_value(template, index = 0)
				templatesToRemove.append(template)

		if bracket is None:
			break

		newBracket = Bracket(templateToReplace, bracket)	
		newBracket.process()
		wikicode.replace(bracket, str(newBracket))

		for template in templatesToRemove:
			remove_and_squash(wikicode, template)

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

	if not BracketHelper.load(templateToReplace):
		pywikibot.stdout("<<lightred>>Missing support for template: " + templateToReplace)
		return

	edit_summary = f'Convert Bracket {templateToReplace} to Match2'
	logging.basicConfig(filename="log_"+templateToReplace.replace('/','_')+".txt", level=logging.INFO)
	generator = genFactory.getCombinedGenerator()
	logging.info("--------"+templateToReplace+"--------")
	for page in generator:
		logging.info("Working on " + page.full_url())
		try:
			text = get_text(page)
			new_text = process_text(text, templateToReplace)
			put_text(page, summary=edit_summary, new=new_text)
		except match2exceptions.VodX:
			logging.error("VodX:"+str(page))
		except match2exceptions.WikiStyle:
			logging.error("WikiStyle:"+str(page))
		except match2exceptions.MalformedScore:
			logging.error("MalformedScore:"+str(page))

if __name__ == '__main__':
	main()