import sys
from typing import Dict

import mwparserfromhell

import pywikibot
from pywikibot import pagegenerators
from scripts.match2.commons.utils import generateId, getMatchGroupForLanguage
from scripts.match2.commons.template import Template
from scripts.utils import get_text, put_text


def processText(bracketClass, text: str, config: Dict[str, str]):
	templateToFind = config['oldTemplateId'] if 'oldTemplateId' in config else 'LegacyBracket'
	wikicode = mwparserfromhell.parse(text)
	for template in wikicode.filter_templates():
		if template.name.matches(templateToFind):
			t = Template(template, removeComments=True)
			t.addIfNotHas('1', config['newTemplateId'])
			t.addIfNotHas('2', config['oldTemplateId'])
			t.addIfNotHas('type', config['bracketType'])
			t.addIfNotHas('id', generateId())

			bracket = bracketClass(t)

			if not bracketClass.isBracketDataAvailable(bracket.newTemplateId):
				pywikibot.stdout("<<lightred>>Missing support for template " + bracket.newTemplateId)
				sys.exit(1)
			wikicode.replace(template, str(bracket))

	return str(wikicode)

def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	isLegacy = True
	save = True
	config: Dict[str, str] = {
		'oldTemplateId': '',
		'newTemplateId': '',
		'bracketType': ''
	}

	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, value = arg.partition(':')
			if arg == 'nosave':
				save = False
			if arg == 'noLegacy':
				isLegacy = False
			if arg == 'oldTemplateId':
				config['oldTemplateId'] = value
			if arg == 'newTemplateId':
				config['newTemplateId'] = value
			if arg == 'bracketType':
				config['bracketType'] = value

	if not isLegacy:
		if not config['oldTemplateId']:
			config['oldTemplateId'] = pywikibot.input('Old template name:')
		if not config['newTemplateId']:
			config['newTemplateId'] =  pywikibot.input('New template name:')
		if not config['bracketType']:
			config['bracketType'] = pywikibot.input('Bracket type:')
	else:
		config = {}

	bracketClass = getMatchGroupForLanguage(genFactory.site.code, 'Bracket')

	editSummary = 'Convert LegacyBracket to Match2'
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = processText(bracketClass, text, config)
		if save:
			put_text(page, summary=editSummary, new=newText)
		else:
			print(newText)

if __name__ == '__main__':
	main()
