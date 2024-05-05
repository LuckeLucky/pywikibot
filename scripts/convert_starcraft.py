import mwparserfromhell

import pywikibot
from pywikibot import pagegenerators
from scripts.match2.commons.template import Template
from scripts.match2.commons.utils import generateId, importClass
from scripts.utils import get_text, put_text, remove_and_squash


MAX_NUMBER_OF_MAPS = 21

singleMatchClass = importClass('starcraft', 'Singlematch')
mapClass = importClass('starcraft', 'Map')

def getSingleMatch(template) -> object:
	t = Template(template)
	t.add('type', 'team')
	t.add('id', generateId())
	t.add('team1', t.getfirstValueFound(['team1', 'team1short', 'team1literal']))
	t.add('team2', t.getfirstValueFound(['team2', 'team2short', 'team2literal']))
	return singleMatchClass(t)

def copyDateAndVod(singleMatch, t):
	if t.getValue('date'):
		singleMatch.match.template.add('date', t.getValue('date'))
	if t.getValue('vod'):
		singleMatch.match.template.add('vod', t.getValue('vod'))

def handleMatchLegacy(singleMatch, nested):

	last = None
	if len(singleMatch.match.maps) > 0:
		last = singleMatch.match.maps[-1]

	lastMapIndex = last.index if last else 0

	previousGroup = int(last.template.getValue('subgroup') if last and last.template.getValue('subgroup') else 0)

	hasSubGroup = False
	added = 0
	for i in range(1, MAX_NUMBER_OF_MAPS):
		mapName = nested.getValue(f'map{i}')
		win = nested.getValue(f'map{i}win')
		if mapName or win:
			lastMapIndex += 1
			newMap = None
			if i == 1:
				newMap = mapClass(lastMapIndex, nested)
				newMap.prefix = ''
			else:
				hasSubGroup = True
				mapTemplate = Template.createFakeTemplate()
				mapTemplate.add(f'map{lastMapIndex}win', win)
				mapTemplate.add(f'map{lastMapIndex}', mapName)
				mapTemplate.add('subgroup', previousGroup + 1)
				mapTemplate.add('validSubgroup', 'true')

				newMap = mapClass(lastMapIndex, mapTemplate)
				newMap.prefix = f'map{lastMapIndex}'
			added += 1
			singleMatch.match.maps.append(newMap)
		else:
			break

	nested.add('subgroup', previousGroup + 1)
	if not hasSubGroup and added == 0:
		lastMapIndex += 1
		newMap = mapClass(lastMapIndex, nested)
		newMap.prefix = ''
		singleMatch.match.maps.append(newMap)

def fixSubGroups(singleMatch):
	hasSubgroups = False
	for map in singleMatch.match.maps:
		if map.template.getValue('validSubgroup'):
			hasSubgroups = True
			break

	if hasSubgroups:
		return

	for map in singleMatch.match.maps:
		if map.template.has('subgroup'):
			map.template.remove('subgroup')


def convert(text: str) -> str:
	while True:
		wikicode = mwparserfromhell.parse(text)
		singleMatch = None
		replace = None
		remove = None
		for template in wikicode.filter_templates():
			if template.name.matches('TeamMatchListHeader'):
				replace = template
				singleMatch = getSingleMatch(template)
			if template.name.matches('LegacyMatchList') and replace is not None:
				remove = template
				t = Template(template)
				first = True
				for key, _ in t.iterateByPrefix('match'):
					nested = Template(t.getNestedTemplate(key))
					if first:
						copyDateAndVod(singleMatch, nested)
						first = False

					handleMatchLegacy(singleMatch, nested)
				break

		if replace is None:
			break

		fixSubGroups(singleMatch)
		wikicode.replace(replace, str(singleMatch))
		if remove:
			remove_and_squash(wikicode, remove)

		text = str(wikicode)

	return str(wikicode)
			


def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	save = True
	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue

	editSummary = 'Convert TeamMatchListHeader to Match2'

	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = convert(text)
		if text != newText:
			if save:
				put_text(page, newText, editSummary)
			else:
				print(newText)

if __name__ == '__main__':
	main()
