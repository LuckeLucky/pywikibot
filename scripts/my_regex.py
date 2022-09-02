import pywikibot
from pywikibot import pagegenerators

import re

import utils

def main(*args):

	# summary message
	edit_summary = 'Move hardcoded color to css class'

	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue

	generator = genFactory.getCombinedGenerator()

	regex = r"style=\"(.*?)background(?:-color):\{\{[Cc]olor\|(.*?)\}\};?"
	subst = "class=\"bg-\\2\" style=\"\\1"
	for page in generator:
		text = utils.get_text(page)
		result = re.sub(regex, subst, text, 0, re.MULTILINE)
		utils.put_text(page, summary=edit_summary, new=result)

if __name__ == '__main__':
	main()