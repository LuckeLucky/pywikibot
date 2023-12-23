import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators

from scripts.match2.factory import getShowmatchClassForLanguage
from scripts.utils import get_text, put_text

def processText(text: str, language: str, old_template_name: str):
	while True :
		wikicode = mwparserfromhell.parse(text)
		showmatchTemplate = None
		for template in wikicode.filter_templates():
			if template.name.matches(old_template_name):
				showmatchTemplate = template

		if showmatchTemplate is None:
			break

		newShowmatch = getShowmatchClassForLanguage(language, showmatchTemplate)
		wikicode.replace(showmatchTemplate, str(newShowmatch))
		text = str(wikicode)

	return text

def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	templateToReplace = ''

	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, value = arg.partition(':')
			if arg == 'template':
				templateToReplace = value

	if not templateToReplace:
		templateToReplace = pywikibot.input('Template to replace:')

	editSummary = 'Convert Showmatch to Match2'
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		lang = page.site.code
		newText = processText(text, lang, templateToReplace)
		put_text(page, summary=editSummary, new=newText)

if __name__ == '__main__':
	main()
