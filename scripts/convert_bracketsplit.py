import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from match2.factory import BracketFactory
from match2.commons.utils import getStringFromTemplate
from scripts.match2.commons.bracket import Bracket
from utils import get_text, put_text, remove_and_squash

def processText(bracketClass: Bracket, text: str, oldTemplateId: str):
	while(True):
		templatesToRemove = []
		wikicode = mwparserfromhell.parse(text)
		bracketTemplate = None
		for template in wikicode.filter_templates():
			if template.name.matches(oldTemplateId):
				bracketTemplate = template

		if bracketTemplate is None:
			break
		bracket2 = bracketClass.createNewBracket(bracketTemplate, oldTemplateId)
		bracket2.newTemplateId = 'Bracket/2-2'
		bracket2.mappingKey = bracket2.newTemplateId + "$$" + oldTemplateId
		bracket2.process()
		bracket2.roundData['R1M1header'] = 'Reseeding Matches'
		bracketq = bracketClass.createNewBracket(bracketTemplate, oldTemplateId)
		bracketq.newTemplateId = 'Bracket/4-2Q'
		bracketq.mappingKey = bracketq.newTemplateId + "$$" + oldTemplateId
		bracketq.process()
		newbracket = '{{box|start|padding=20px}}\n' + str(bracket2) + '\n{{box|break}}\n' + str(bracketq) + '\n{{box|end}}\n'
		wikicode.replace(bracketTemplate, newbracket)

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

	bracketClass: Bracket = BracketFactory.getBracketClassForLanguage(language)

	if not bracketClass.isAliasSet(oldTemplateId):
		pywikibot.stdout("<<lightred>>Missing support for template: " + oldTemplateId)
		exit(1)

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