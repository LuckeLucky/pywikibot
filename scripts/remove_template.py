import pywikibot
import mwparserfromhell
from pywikibot import pagegenerators

from scripts.utils import get_text, put_text, remove_and_squash

def process(text: str, templateId: str) -> str:
	wikicode = mwparserfromhell.parse(text)
	for template in wikicode.filter_templates(
		matches=lambda t: str(t.name).rstrip() == templateId
	):
		remove_and_squash(wikicode, template)

	return str(wikicode)


def main(*args):
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	templateId = None
	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, value = arg.partition(':')
			if arg == 'templateId':
				templateId = value

	if not templateId:
		templateId = pywikibot.input('TemplateId:')

	editSummary = f'Remove template {templateId}'

	generator = genFactory.getCombinedGenerator()
	for page in generator:
		oldText = get_text(page)
		newText = process(oldText, templateId)
		if newText != oldText:
			put_text(page, newText, editSummary)
		else:
			pywikibot.info(f'No changes were necessary in {page}')

if __name__ == '__main__':
	main()
