import pywikibot
import mwparserfromhell

from pywikibot import pagegenerators
from mwparserfromhell.nodes import Template
from mwparserfromhell.nodes.extras import Parameter
from utils import get_text, put_text
from match2.commons.utils import generateId

def renameTemplateAndAddId(oldTemplate: Template, oldTemplateId: str, newTemplateId: str, bracketType:str):
	strTemplate = str(oldTemplate)
	newTemplate = strTemplate.replace(oldTemplateId, f'LegacyBracket|{newTemplateId}|{oldTemplateId}|type={bracketType}|id={generateId()}')
	return newTemplate

def processText(text: str, oldTemplateId: str, newTemplateId: str, bracketType: str):
	wikicode = mwparserfromhell.parse(text)
	for template in wikicode.filter_templates():
		if template.name.matches(oldTemplateId):
			newTemplate = renameTemplateAndAddId(template, oldTemplateId, newTemplateId, bracketType)
			wikicode.replace(template, newTemplate)

	return str(wikicode)

def main(*args):
	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	oldTemplateId = ''
	newTemplateId = ''
	bracketType = ''

	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, value = arg.partition(':')
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

	if not bracketType:
		bracketType = pywikibot.input('Type:')

	if bracketType not in ['team', 'solo']:
		pywikibot.stdout("<<lightred>>bracket type error")

	editSummary = f'Convert {oldTemplateId} to Legacy Version'
			
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		if not page.has_permission():
			continue
		text = get_text(page)
		new_text = processText(text, oldTemplateId, newTemplateId, bracketType)
		put_text(page, summary=editSummary, new=new_text)

if __name__ == '__main__':
	main()