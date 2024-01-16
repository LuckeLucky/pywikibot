from typing import Dict, List

import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators
from scripts.match2.commons.template import Template
from scripts.match2.valorant.bracket import BracketValorant
from scripts.utils import get_text, put_text, remove_and_squash

from scripts.match2.commons.opponent import Opponent, TeamOpponent

def addStuffToTemplate(keys: Dict[str, str], newTemplate:Template, oldTemplate:Template) -> Opponent:
	zdetails = Template(oldTemplate.getNestedTemplate(keys['oldDetails']+'_zdetails'))
	newTemplate.add(keys['opp1'] + 'team', zdetails.getValue('team1'))
	newTemplate.add(keys['opp2'] + 'team', zdetails.getValue('team2'))
	newTemplate.add(keys['opp1'] + 'score', oldTemplate.getValue(keys['oldDetails']+'_p1score'))
	newTemplate.add(keys['opp2'] + 'score', oldTemplate.getValue(keys['oldDetails']+'_p2score'))
	newTemplate.add(keys['details'] + 'details', zdetails.getNestedTemplate('details'))

def processText(text: str):
	wikicode = mwparserfromhell.parse(text)
	templates: List[Template] = []
	shit = []
	#first is upper bracket
	#second is lower bracket Round 1 and first game R2
	#third is second game R2
	#forth is R3
	#fifth is R4
	#last is gf
	for template in wikicode.filter_templates():
		t = Template(template)
		name = str(t.name).strip()
		if name.startswith('#invoke:LosersBracketStructure'):
			templates.append(t)
		if name.startswith('#invoke:Bracket'):
			if t.getValue(index=0) == 'GrandFinals':
				templates.append(t)
		if name.startswith('#invoke:'):
			shit.append(template)

	wtf = Template.createFakeTemplate()
	wtf.name = 'WTF'
	#Round 1 upper
	addStuffToTemplate({'opp1': 'R1D1', 'opp2': 'R1D2', 'details': 'R1G1', 'oldDetails': 'R1G1'}, wtf, templates[0])
	addStuffToTemplate({'opp1': 'R1D3', 'opp2': 'R1D4', 'details': 'R1G2', 'oldDetails': 'R1G2'}, wtf, templates[0])
	addStuffToTemplate({'opp1': 'R1D5', 'opp2': 'R1D6', 'details': 'R1G3', 'oldDetails': 'R1G3'}, wtf, templates[0])
	addStuffToTemplate({'opp1': 'R1D7', 'opp2': 'R1D8', 'details': 'R1G4', 'oldDetails': 'R1G4'}, wtf, templates[0])
	#Round 2 upper
	addStuffToTemplate({'opp1': 'R2W1', 'opp2': 'R2W2', 'details': 'R2G1', 'oldDetails': 'R2G1'}, wtf, templates[0])
	addStuffToTemplate({'opp1': 'R2W3', 'opp2': 'R2W4', 'details': 'R2G2', 'oldDetails': 'R2G2'}, wtf, templates[0])
	#Round 4 upper
	addStuffToTemplate({'opp1': 'R4W1', 'opp2': 'R4W2', 'details': 'R4G1', 'oldDetails': 'R4G1'}, wtf, templates[0])
	#Round 1 lower
	addStuffToTemplate({'opp1': 'R1D9', 'opp2': 'R1D10', 'details': 'R1G5', 'oldDetails': 'R1G1'}, wtf, templates[1])
	addStuffToTemplate({'opp1': 'R1D11', 'opp2': 'R1D12', 'details': 'R1G6', 'oldDetails': 'R1G2'}, wtf, templates[1])
	#Round 2 lower
	addStuffToTemplate({'opp1': 'R2W5', 'opp2': 'R2W6', 'details': 'R2G3', 'oldDetails': 'R2G1'}, wtf, templates[1])
	addStuffToTemplate({'opp1': 'R2D1', 'opp2': 'R2D2', 'details': 'R2G4', 'oldDetails': 'R1G1'}, wtf, templates[2])
	#Round 3 lower
	addStuffToTemplate({'opp1': 'R3W1', 'opp2': 'R3W2', 'details': 'R3G1', 'oldDetails': 'R3G1'}, wtf, templates[3])
	#Round 4 lower
	addStuffToTemplate({'opp1': 'R4D1', 'opp2': 'R4W3', 'details': 'R4G2', 'oldDetails': 'R1G1'}, wtf, templates[4])
	#gf
	addStuffToTemplate({'opp1': 'R5W1', 'opp2': 'R5W2', 'details': 'R5G1', 'oldDetails': 'R5G1'}, wtf, templates[5])

	bracket = BracketValorant(wtf)
	bracket.newTemplateId = 'Bracket/8U4H2LL1D'
	bracket.oldTemplateId = 'WTF'
	bracket.bracketType = 'team'
	bracket.mappingKey = bracket.newTemplateId + "$$" + bracket.oldTemplateId
	bracket.process()

	wikicode.replace(shit[0], str(bracket))
	shit = shit[1:]

	for template in shit:
		remove_and_squash(wikicode, template)

	return str(wikicode)


def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue

	editSummary = 'Convert invokeMess to Match2'
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = processText(text)
		put_text(page, newText, editSummary)



if __name__ == '__main__':
	main()
