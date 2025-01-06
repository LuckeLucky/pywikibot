import sys

import mwparserfromhell

import pywikibot
from pywikibot import pagegenerators
from scripts.utils import get_text, put_text

MATCHGROUPS = ['singlematch', 'matchlist', 'bracket']

def invokeJson(template: mwparserfromhell.nodes.Template, newTemplateId: str) -> str:
	newTemplateId += '|R1G1=' + str(template) + '}}'
	newTemplateId = newTemplateId.replace('={{', '={{subst:#invoke:Json|fromArgs|templateName=')

	return newTemplateId

def convert(oldTemplateId: str, newTemplateId: str, text: str) -> str:
	wikicode = mwparserfromhell.parse(text)
	for t in wikicode.filter_templates(matches = lambda t: t.name.matches(oldTemplateId)):
		wikicode.replace(t, invokeJson(t, newTemplateId))

	return str(wikicode)

def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	save = True
	m1Args = {
		'oldTemplateId': None,
		'matchGroupType': None,
		'opponentType': None,
		'newBracketId': None
	}
	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg, _, value = arg.partition(':')
			arg = arg[1:]
			if arg == 'nosave':
				save = False
			elif arg in m1Args and m1Args[arg] is None:
				m1Args[arg] = value

	m1Args['matchGroupType'] = m1Args['matchGroupType'] if m1Args['matchGroupType'] is not None\
		else pywikibot.input('Argument matchGroupType is required, input value:')
	if m1Args['matchGroupType'] != "bracket":
		del m1Args['newBracketId']

	newTemplateId = '{{subst:#invoke:M1Conversion/Custom|run'
	for key, value in m1Args.items():
		if value is None:
			value = pywikibot.input(f'Argument {key} is required, input value:')
			m1Args[key] = value
		newTemplateId += f'|{key}={value}'

	if m1Args['matchGroupType'] not in MATCHGROUPS:
		pywikibot.stdout("Invalid matchGroup, one of " + ','.join(MATCHGROUPS))
		sys.exit(1)

	editSummary = f'Convert {m1Args["oldTemplateId"]} to Match2'
	oldTemplateId = m1Args['oldTemplateId']

	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = convert(oldTemplateId, newTemplateId, text)
		if text != newText:
			if save:
				put_text(page, newText, editSummary)
			else:
				print(newText)

if __name__ == '__main__':
	main()
