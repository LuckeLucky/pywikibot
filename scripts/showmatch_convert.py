import logging
import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from match2conversion.showmatch import Showmatch
from scripts.match2conversion import match2exceptions
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
	logging.basicConfig(filename="log_Showmath.txt", level=logging.INFO)
	for page in generator:
		logging.info("Working on " + page.full_url())
		try:
			text = get_text(page)
			new_text = process_text(text)
			put_text(page, summary=edit_summary, new=new_text)
		except match2exceptions.VodX:
			logging.error("VodX:"+str(page))
		except match2exceptions.WikiStyle:
			logging.error("WikiStyle:"+str(page))
		except match2exceptions.MalformedScore:
			logging.error("MalformedScore:"+str(page))

if __name__ == '__main__':
	main()