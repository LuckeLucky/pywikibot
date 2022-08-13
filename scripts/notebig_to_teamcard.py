from pipes import Template
import re
import utils
import mwparserfromhell
import pywikibot

from datetime import datetime
from pywikibot import pagegenerators

REGEX_INDEX = r'n(\d*)'
REGEX_SPAN = r'<span .*>(.*?)</span>'

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
	if noteBig is None:
		return {}
	indexedNotes = {}
	for parameter in noteBig.params:
		if str(parameter.name) == 'nobox':
			continue
		findIndex = re.search(REGEX_INDEX, str(parameter.name))
		if findIndex:
			index = findIndex.group(1)
			value = str(parameter.value)
			if not (' - ' in value):
				date = get_date(value)
				if date:
					value = date + ' - ' + value
			indexedNotes[index] = value
	return indexedNotes

def notebig_to_teamcards(teamCards: list, notes: dict):
	if (not teamCards) or (not notes):
		return
	x = []
	notesInserted = 0
	notesDuplicated = 0
	for teamCard in teamCards:
		if teamCard.has('notes'):
			noteIDs = str(teamCard.get('notes').value)
			if len(noteIDs) == 0 or noteIDs == '\n':
				continue
			span = re.search(REGEX_SPAN, noteIDs)
			if span:
				noteIDs = span.group(1)
			
			iNotes = '{{NoteBig\n'
			index = 1
			for noteID in noteIDs.split(', '):
				id = noteID.rstrip()
				text = notes[id]
				iNotes = iNotes + '|n' + str(index) + '='
				if not id in x:
					x.append(id)
					iNotes = iNotes + text
					notesInserted += 1
				else:
					iNotes = iNotes + '(USE_REF_NAME)' + text
					notesDuplicated += 1
				index += 1

			iNotes = iNotes + '}}'

			teamCard.remove('notes')
			teamCard.add('inotes', iNotes)

	print("Notes Moved:" + str(len(x)))
	print("Notes Duplicated:" + str(notesDuplicated))
	for id, text in notes.items():
		if id not in x:
			print(id + "refering to ?")

def process_text(text: str):
	wikicode = mwparserfromhell.parse(text)

	teamCards = []
	noteBig = None
	for template in wikicode.filter_templates():
		if template.name.matches('TeamCard') or template.name.matches('TeamCardLeague'):
			teamCards.append(template)
		if template.name.matches('NoteBig'):
			noteBig = template

	indexedNotes = notebig_to_dict(noteBig)

	print("Notes Found:" + str(len(indexedNotes)))
	templatesToRemove = []
	for template in wikicode.filter_templates():
		if template.name.matches('NoteBig'):
			templatesToRemove.append(template)
		if template.name.matches('roster changes start'):
			templatesToRemove.append(template)
		if template.name.matches('roster changes end'):
			templatesToRemove.append(template)

	for template in templatesToRemove:
		utils.remove_and_squash(wikicode, template)

	notebig_to_teamcards(teamCards, indexedNotes)

	return str(wikicode)

def main(*args):
	# summary message
	edit_summary = 'Move NoteBig to Teamcard'

	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()
	save = False
	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue
		if arg == '-save':
			save = True

	generator = genFactory.getCombinedGenerator()

	for page in generator:
		original_text = utils.get_text(page)
		new_text = process_text(original_text)
		if save:
			utils.put_text(page, summary=edit_summary, new=new_text)


if __name__ == '__main__':
	main()