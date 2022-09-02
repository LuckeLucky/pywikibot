import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from match2conversion.showmatch import Showmatch
from utils import get_text, put_text

def process_text(text: str):
	while(True):
		wikicode = mwparserfromhell.parse(text)

		showmatchTemplate = None
		for template in wikicode.filter_templates():
			if template.name.matches('Showmatch'):
				showmatchTemplate = template
		
		if showmatchTemplate is None:
			break

		newShowmatch = Showmatch(showmatchTemplate)
		newShowmatch.process()
		wikicode.replace(showmatchTemplate, str(newShowmatch))
		text = str(wikicode)

	return text

def main(*args):

	# summary message
	edit_summary = 'Convert Showmatch to Match2'

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
		print(new_text)
		#put_text(page, summary=edit_summary, new=new_text)

if __name__ == '__main__':
	main()