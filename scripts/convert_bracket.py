import sys
from typing import Dict

import mwparserfromhell

import pywikibot
from pywikibot import pagegenerators
from scripts.match2.commons.template import Template
from scripts.match2.factory import getBracketClassForLanguage
from scripts.utils import get_text, put_text


def processText(bracketClass, text: str, config: Dict[str, str]):
	while True:
		wikicode = mwparserfromhell.parse(text)
		legacyBracket = None
		for template in wikicode.filter_templates():
			if (template.name.matches('LegacyBracket') or
				(config is not None and template.name.matches(config['oldTemplateId']))):
				legacyBracket = template
				break

		if legacyBracket is None:
			break
		newBracket = bracketClass(Template(legacyBracket, removeComments=True))
		if config is not None:
			newBracket.newTemplateId = config['newTemplateId']
			newBracket.oldTemplateId = config['oldTemplateId']
			newBracket.bracketType = config['bracketType']
			newBracket.mappingKey = newBracket.newTemplateId + "$$" + newBracket.oldTemplateId

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
		config = None

	language = genFactory.site.code
	if not language:
		return

	bracketClass = getBracketClassForLanguage(language)

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
