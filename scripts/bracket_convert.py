import pywikibot
import mwparserfromhell

from pywikibot import pagegenerators

from scripts.match2conversion.bracket import Bracket
from utils import get_text, put_text

def process_text(text: str):
	wikicode = mwparserfromhell.parse(text)
	bracket = None
	for template in wikicode.filter_templates():
		if template.name.matches('32DETeamBracket'):
			bracket = template
	
	newBracket = Bracket('32DETeamBracket', bracket)
	
	wikicode.replace(bracket, str(newBracket))

	return wikicode

def main(*args):

    # summary message
    edit_summary = 'Converting Brackets to Match2'

    # Read commandline parameters.
    local_args = pywikibot.handle_args(args)
    genFactory = pagegenerators.GeneratorFactory()

    for arg in local_args:
        if genFactory.handle_arg(arg):
            continue

    generator = genFactory.getCombinedGenerator()

    for page in generator:
        text = get_text(page)
        new_text = process_text(text)
        put_text(page, summary=edit_summary, new=new_text)

if __name__ == '__main__':
    main()