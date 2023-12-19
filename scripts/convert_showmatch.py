import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from match2.factory import ShowmatchFactory
from utils import get_text, put_text

def process_text(text: str, language: str, old_template_name: str):
	while(True):
		wikicode = mwparserfromhell.parse(text)

		showmatchTemplate = None
		for template in wikicode.filter_templates():
			if template.name.matches(old_template_name):
				showmatchTemplate = template
		
		if showmatchTemplate is None:
			break

		newShowmatch = ShowmatchFactory.getShowmatchClassForLanguage(language, showmatchTemplate)
		wikicode.replace(showmatchTemplate, str(newShowmatch))
		text = str(wikicode)

	return text

def main(*args):

	# summary message
	edit_summary = 'Convert Showmatch to Match2'

	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	templateToReplace = ''

	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, value = arg.partition(':')
			if arg == 'template':
				templateToReplace = value

	if not templateToReplace:
		templateToReplace = pywikibot.input('Template to replace:')

	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		lang = page.site.code
		new_text = process_text(text, lang, templateToReplace)
		put_text(page, summary=edit_summary, new=new_text)

if __name__ == '__main__':
	main()