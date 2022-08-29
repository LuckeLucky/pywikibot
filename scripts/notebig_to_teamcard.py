import re
import utils
import mwparserfromhell
import pywikibot

from datetime import datetime
from pywikibot import pagegenerators

""" Known bugs
	-Fail to close wikicode tags cause parameter to be skiped
	- ex-Team in start of frase can cause date to not be addded """

REGEX_INDEX = r'n(\d*)'
REGEX_SPAN = r'<span .*>(.*?)</span>'

#Returns day ordinal
def day_to_ordinal(day: str) -> str:
	intDay = int(day)

	suffix = ''
	if 4 <= intDay <= 20 or 24 <= intDay <= 30:
		suffix = "th"
	else:
		suffix = ["st", "nd", "rd"][intDay % 10 - 1]

	if day.startswith('0'):
		day = day[1:]

	return day + suffix

#Returns the date in format Month Day from a cite_web template
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
			#Check if note has string Month Day - 
			dateString = value[:21]
			if not ('-' in dateString):
				date = get_date(value)
				if date:
					value = date + ' - ' + value
			indexedNotes[index] = value
	return indexedNotes

#Sets the teamcards inotes using notes found in notebig template
def set_teamcard_inotes(teamCards: list, foundNotes: dict) -> int:
	if (not teamCards) or (not foundNotes):
		return
	notesAdded = []
	notesInserted = 0
	notesDuplicated = 0
	for teamCard in teamCards:
		if teamCard.has('notes'):
			noteIDs = str(teamCard.get('notes').value)
			if len(noteIDs) == 0 or noteIDs == '\n':
				continue

			iNotes = '{{NoteBig\n'
			inotesIndex = 1

			#Split notes
			splittedNotes = []
			if ', ' in noteIDs:
				splittedNotes = noteIDs.split(', ')
			elif '&' in noteIDs:
				splittedNotes = noteIDs.split('& ')
			else:
				splittedNotes = noteIDs.split(',')
			#Each note number
			for noteID in splittedNotes:
				id = noteID.rstrip()
				id = id.lstrip()
				if id not in foundNotes:
					print("Note ["+ id + "] missing in NoteBig")
					return -1
				text = foundNotes[id]
				iNotes = iNotes + '|n' + str(inotesIndex) + '='

				if not id in notesAdded:
					notesAdded.append(id)
					iNotes = iNotes + text
					notesInserted += 1
				else:
					iNotes = iNotes + '(USE_REF_NAME)' + text
					notesDuplicated += 1
				inotesIndex += 1

			iNotes = iNotes + '}}'

			teamCard.remove('notes')
			teamCard.add('inotes', iNotes)

	print("Notes Moved:" + str(len(notesAdded)))
	print("Notes Duplicated:" + str(notesDuplicated))

	#Find notes present in NoteBig but not on teamCardNotes
	for id, text in foundNotes.items():
		if id not in notesAdded:
			print("Note ["+ id + "] missing in TeamCard")

	return len(notesAdded)

def process_text(text: str):
	wikicode = mwparserfromhell.parse(text)

	teamCards = []
	noteBig = None
	countNoteBigFound = 0
	for template in wikicode.filter_templates():
		if (template.name.matches('TeamCard') or
			template.name.matches('TeamCardLeague') or
			template.name.matches('TeamCardMix') or 
			template.name.matches('TeamCardSubs')):
			teamCards.append(template)
		if template.name.matches('NoteBig') or template.name.matches('note15'):
			noteBig = template
			countNoteBigFound +=1

	foundNotes = notebig_to_dict(noteBig)

	print("Notes Found:" + str(len(foundNotes)))

	#Remove templates
	templatesToRemove = []
	for template in wikicode.filter_templates():
		if template.name.matches('NoteBig') or template.name.matches('note15'):
			templatesToRemove.append(template)
		if template.name.matches('roster changes start'):
			templatesToRemove.append(template)
		if template.name.matches('roster changes end'):
			templatesToRemove.append(template)

	for template in templatesToRemove:
		utils.remove_and_squash(wikicode, template)
	#Set inotes
	notesMoved = set_teamcard_inotes(teamCards, foundNotes)

	if notesMoved != len(foundNotes):
		return ''
	return str(wikicode)

def main(*args):
	# summary message
	editSummary = 'Move NoteBig to Teamcard'

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
		originalText = utils.get_text(page)
		print(page.full_url())

		newText = process_text(originalText)

		if newText == '':
			print("FIX NOTES FOUND")
		else:
			if save:
				utils.put_text(page, summary=editSummary, new=newText)
			else:
				answer = input("Wanna save?(y/n)")
				if answer.lower() == 'y':
					utils.put_text(page, summary=editSummary, new=newText)


if __name__ == '__main__':
	main()