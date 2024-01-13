import mwparserfromhell
import pywikibot
import re

from mwparserfromhell.nodes import Template, ExternalLink

from pywikibot import pagegenerators
from scripts.utils import get_text, put_text

def processStreamTable(tag) -> str:
	wikicode = mwparserfromhell.parse(tag)
	flags = wikicode.filter_templates()
	externalLinks = wikicode.filter_external_links()
	if len(flags) != len(externalLinks):
		return ''
	flag: Template
	externalLink: ExternalLink
	index = 1
	out = '{{Streams\n'
	for flag, externalLink in zip(flags, externalLinks):
		lang = str(flag.name).split('/')
		if len(lang) < 2:
			return ''
		out += f'|lang{index}={lang[-1]} '
		urlParts = re.findall(r"(?:www|play|https?://)\.*(\w*)\.(?:tv|com|live)/(.*)", str(externalLink.url))
		if len(urlParts) == 0:
			return ''
		domain, channel = urlParts[0]
		if domain == 'afreecatv':
			domain = 'afreeca'
		out += f'|{domain}{index}={channel}\n'
		index += 1

	out += '}}'
	return out



def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue

	generator = genFactory.getCombinedGenerator()
	for page in generator:
		oldText = get_text(page)
		wikicode = mwparserfromhell.parse(oldText)
		for tag in wikicode.filter_tags(matches=lambda node: node.tag == "table"):
			if 'Stream' in tag:
				streamTemplate = processStreamTable(str(tag))
				if streamTemplate:
					wikicode.replace(tag, streamTemplate)

		newText = str(wikicode)
		if newText == oldText:
			pywikibot.info(f'No changes were necessary in {page}')
			continue
		pywikibot.showDiff(oldText, newText, context=0)
		put_text(page, newText, 'Move Streams to template')

if __name__ == '__main__':
	main()