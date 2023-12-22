import pywikibot
import mwparserfromhell
import random
import string

from pywikibot import pagegenerators
from mwparserfromhell.nodes import Template
from mwparserfromhell.nodes.extras import Parameter
from utils import get_text, put_text
from .match2.commons.utils import generateId

def renameTemplateAndAddId(oldTemplate: Template, newTemplateId: str):
	newTemplate = Template(newTemplateId, oldTemplate.params)
	param = Parameter('id', generateId())
	newTemplate.params.insert(0, param)
	return newTemplate

def processText(text: str, oldTemplateId: str, newTemplateId: str):
	wikicode = mwparserfromhell.parse(text)
	for template in wikicode.filter_templates():
		if template.name.matches(oldTemplateId):
			newTemplate = renameTemplateAndAddId(template, newTemplateId)
			wikicode.replace(template, newTemplate)

	return str(wikicode)

def main(*args):
	# summary message
	edit_summary = 'Convert old MatchList to Legacy Version'

	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	oldTemplateId = ''
	newTemplateId = ''

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
	
	if not oldTemplateId:
		oldTemplateId = pywikibot.input('Old template name:')

	if not newTemplateId:
		newTemplateId = pywikibot.input('New template name:')
			
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		if not page.has_permission():
			continue
		text = get_text(page)
		new_text = processText(text, oldTemplateId, newTemplateId)
		put_text(page, summary=edit_summary, new=new_text)

if __name__ == '__main__':
	main()