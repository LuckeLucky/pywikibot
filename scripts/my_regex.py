import pywikibot
from pywikibot import pagegenerators

import re

import utils

def main(*args):

	# summary message
	edit_summary = 'Fix order of side input'

	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue

	generator = genFactory.getCombinedGenerator()

	regex = r"\|(o\d*|)?t1firstside=(t|ct)?\|(o\d*|)?t1ct=(\d*)?\|(o\d*|)?t1t=(\d*)?\|(o\d*|)?t2ct=(\d*)?\|(o\d*|)?t2t=(\d*)?"
	subst = "|\\1t1firstside=\\2|\\3t1t=\\6|\\5t1ct=\\4|\\7t2t=\\g<10>|\\9t2ct=\\8"
	for page in generator:
		text = utils.get_text(page)
		result = re.sub(regex, subst, text, 0, re.MULTILINE)
		utils.put_text(page, summary=edit_summary, new=result)

if __name__ == '__main__':
    main()