import re
import utils
import mwparserfromhell
import pywikibot

from datetime import datetime
from pywikibot import pagegenerators

REGEX_INDEX = r'n(\d*)'
REGEX_UNTIL_FULL_STOP = r'([^.]+)'
REGEX_DATE = r'^(\w* \d*\w*) - '
REGEX_REF = r'<ref .*>(.*?)</ref>'

def day_to_ordinal(day: str):
	intDay = int(day)

	suffix = ''
	if 4 <= intDay <= 20 or 24 <= intDay <= 30:
		suffix = "th"
	else:
		suffix = ["st", "nd", "rd"][intDay % 10 - 1]

	if day.startswith('0'):
		day = day[1:]

	return day + suffix

def get_date(text: str):
	wikicode = mwparserfromhell.parse(text)
	for template in wikicode.filter_templates():
		if template.name.matches('cite web'):
			if template.has('date'):
				date = str(template.get('date').value).rstrip()
				dt = datetime.strptime(date, '%Y-%m-%d')
				month = dt.strftime('%B')
				day = day_to_ordinal(dt.strftime('%d'))
				return month + ' ' + day

	return ''


def notebig_to_dict(noteBig: mwparserfromhell.nodes.Template) -> dict:
	indexedNotes = {}
	for parameter in noteBig.params:
		findIndex = re.search(REGEX_INDEX, str(parameter.name))
		if findIndex:
			index = findIndex.group(1)
			value = str(parameter.value)
			if not (' - ' in value):
				date = get_date(value)
				value = date + ' - ' + value
			indexedNotes[index] = value
	return indexedNotes


def process_text(text: str):
	wikicode = mwparserfromhell.parse(text)

	noteBig = None
	for template in wikicode.filter_templates():
		if template.name.matches('NoteBig'):
			noteBig = template

	indexedNotes = notebig_to_dict(noteBig)
	print(indexedNotes['1'])


def main(*args):
	# summary message
	""" edit_summary = 'Move NoteBig to Teamcard'

	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue

	generator = genFactory.getCombinedGenerator()

	for page in generator:
		text = utils.get_text(page)
		new_text = process_text(text)
		utils.put_text(page, summary=edit_summary, new=new_text) """

	text = ''
	with open('input.txt', 'r') as file:
		text = file.read()
	new_text = process_text(text)

if __name__ == '__main__':
	main()