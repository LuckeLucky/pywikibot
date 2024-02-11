import mwparserfromhell
import pywikibot

import wikitextparser as wtp

from pywikibot import pagegenerators

from scripts.utils import get_text, put_text

def processHeader(row) -> str:
	eventIndex = 1
	out = '{{Points start|title=Top 12'
	for cell in row:
		if cell in ['#', 'Team', 'Σ']:
			continue
		if cell.startswith('[['):
			wl = wtp.WikiLink(cell)
			out += f"|event{eventIndex}={wl.text}|event{eventIndex}link={wl.title}"
			eventIndex += 1
		else:
			out += f"|event{eventIndex}={cell}"
			eventIndex += 1
	return out + '}}'

def processRow(row) -> str:
	pointsIndex = 1
	out = '{{Points slot'
	place = ''
	for cellIndex, cell in enumerate(row):
		cell = cell.replace('\'', '')
		if cellIndex == 0:
			place += f'|place={cell}'
		elif cellIndex == 1:
			teamTemplate = wtp.Template(cell)
			out += f'|bg=|{teamTemplate.arguments[0].value}' + place
		elif cellIndex == len(row)-1:
			out += f'|total={cell}'
		else:
			out += f'|points{pointsIndex}={cell}'
			pointsIndex+= 1
	return out + '}}'

def processTable(tag: str) -> str:
	table = wtp.Table(tag)
	first = True
	out = ''
	for row in table.data():
		if first:
			out += processHeader(row) + '\n'
			first = False
		else:
			out += processRow(row) + '\n'
	out += '{{Points end}}\n'
	return out

def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue

	generator = genFactory.getCombinedGenerator()
	for page in generator:
		oldText = get_text(page)
		wikicode = mwparserfromhell.parse(oldText)
		for tag in wikicode.filter_tags(matches=lambda node: node.tag == "table"):
			t = processTable(str(tag))
			if t:
				wikicode.replace(tag, t)

		newText = str(wikicode)
		if newText == oldText:
			pywikibot.info(f'No changes were necessary in {page}')
			continue
		pywikibot.showDiff(oldText, newText, context=0)
		put_text(page, newText, 'Move Points table to template')

if __name__ == '__main__':
	main()