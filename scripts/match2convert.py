from match2conversion import Match, Opponent, MatchList, sanitize_template

import mwparserfromhell
from mwparserfromhell.nodes import Template

import pywikibot
from pywikibot import pagegenerators

import utils

MAX_OPPONENTS = 2

def get_opponent(matchMap: Template, index: int):
	team = ''
	score = ''
	if matchMap.has('team' + str(index)):
		team = str(matchMap.get('team' + str(index)).value)
	if matchMap.has('games' + str(index)):
		score = str(matchMap.get('games' + str(index)).value)

	return Opponent(team, score)

def generate_output(matchLists: list, matchMaps: dict) -> list:

	newMatchLists = []
	for matchListIndex, matchListStart in enumerate(matchLists):
		sanitize_template(matchListStart)
		ml = MatchList()

		if matchListStart.has('title'):
			ml.set_title(str(matchListStart.get('title').value))
		if matchListStart.has('matchsection'):
			ml.set_matchsection(str(matchListStart.get('matchsection').value))
		if matchListStart.has('width'):
			ml.set_width(str(matchListStart.get('width').value))
		if matchListStart.has('hide'):
			ml.set_collapsed(str(matchListStart.get('hide').value))
		if matchListStart.has('attached'):
			ml.set_attached(str(matchListStart.get('attached').value))
		if matchListStart.has('gsl'):
			ml.set_gsl(str(matchListStart.get('gsl').value))

		for matchIndex, matchMap in enumerate(matchMaps[matchListIndex]):
			sanitize_template(matchMap)

			#Sometimes date in {{MatchMaps}} can represent a round title
			if matchMap.has('date'):
				ml.add_header(matchIndex + 1, str(matchMap.get('date').value))

			opponent1 = get_opponent(matchMap, 1)
			opponent2 = get_opponent(matchMap, 2)

			match = Match(opponent1, opponent2)
			
			if matchMap.has("details"):
				matchDetails = matchMap.get("details").value.filter_templates()[0]
				sanitize_template(matchDetails)

				match.set_summary(matchDetails)
			
			match.process()
			ml.add_match(match)


		newMatchLists.append(str(ml))

	return newMatchLists


def process_text(text: str):

	wikicode = mwparserfromhell.parse(text)

	matchLists = []
	matchMaps = {}
	matchListIndex = -1
	previousTemplate = None
	for template in wikicode.filter_templates():
		if template.name.matches('MatchListStart'):
			if previousTemplate:
				if previousTemplate.name.matches('GroupTableLeague'):
					template.add('attached', 'true')
			matchLists.append(template)
			matchListIndex += 1
			matchMaps[matchListIndex] = []

		if template.name.matches("MatchMaps"):
			matchMaps[matchListIndex].append(template)

		previousTemplate = template

	newML = generate_output(matchLists, matchMaps)

	# new matchlists replace matchliststart position
	for nodeIndex, node in enumerate(matchLists):
		wikicode.replace(node, newML[nodeIndex])

	#remove old templates that were not replaced
	templatesToRemove = []
	for template in wikicode.filter_templates():
		if template.name.matches('MatchMaps'):
			templatesToRemove.append(template)
		if template.name.matches('MatchListEnd'):
			templatesToRemove.append(template)

	for template in templatesToRemove:
		utils.remove_and_squash(wikicode,template)

	return wikicode

def main(*args):

    # summary message
    edit_summary = 'Converting MatchLists to Match2'

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
        utils.put_text(page, summary=edit_summary, new=new_text)

if __name__ == '__main__':
    main()