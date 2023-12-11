import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from match2.factory import BracketFactory
from match2.commons.utils import get_parameter_str
from utils import get_text, put_text, remove_and_squash

def processText(bracketClass, text: str, oldTemplateId: str):
	shortNames = ''
	while(True):
		templatesToRemove = []
		wikicode = mwparserfromhell.parse(text)
		bracket = None
		for template in wikicode.filter_templates():
			templateName = str(template.name).strip()
			if template.name.matches(oldTemplateId):
				bracket = template
				if shortNames:
					bracket.add('shortNames', shortNames)
			if templateName == '#vardefine:bracket_short_teams':
				shortNames = get_parameter_str(template, index = 0)
				templatesToRemove.append(template)

		if bracket is None:
			break
		newBracket = bracketClass(oldTemplateId, bracket)
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

	oldTemplateId = ''
	save = True

	for arg in local_args:
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

	bracketClass = BracketFactory.getBracketClassForLanguage(language)

	if not bracketClass.load(oldTemplateId):
		pywikibot.stdout("<<lightred>>Missing support for template: " + oldTemplateId)
		return

	edit_summary = f'Convert Bracket {oldTemplateId} to Match2'
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = processText(bracketClass, text, oldTemplateId)
		if save:
			put_text(page, summary=edit_summary, new=newText)
		else:
			print(newText)

if __name__ == '__main__':
	main()