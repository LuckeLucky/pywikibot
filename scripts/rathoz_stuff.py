import pywikibot

from pywikibot import pagegenerators
from scripts.utils import get_text, put_text

def processText(text: str, replaceKeyword: str) -> str:
	while True:
		try:
			startIndex = text.index('{{#smt:')
		except ValueError:
			break

		openBrackets = 0
		currentIndex = startIndex
		textlength = len(text)
		while currentIndex < textlength:
			char = text[currentIndex]
			if char == '{':
				openBrackets += 1
			elif char == '}':
				openBrackets -= 1
			currentIndex += 1
			if openBrackets == 0:
				break
		wikiFunc = text[startIndex:currentIndex]
		wikiFunc = wikiFunc.replace('#smt:', '#invoke:smt|')
		wikiFunc = wikiFunc.replace(replaceKeyword, '<nowiki>' + replaceKeyword)
		wikiFunc = wikiFunc[:-2] + '</nowiki>}}'

		text = text[:startIndex] + wikiFunc + text[currentIndex:]

	return text

def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	prependAt = ''
	summary = ''
	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, value = arg.partition(':')
			if arg == 'prependAt':
				prependAt = value
			if arg == 'summary':
				summary = value

	prependAt = prependAt or pywikibot.input('Prepend at:')
	summary = summary or pywikibot.input('Edit summary')

	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = processText(text, prependAt)
		if text != newText:
			put_text(page, newText, summary)


if __name__ == '__main__':
	main()
