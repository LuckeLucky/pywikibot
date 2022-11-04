
import pywikibot
import mwparserfromhell
from pywikibot import pagegenerators
from scripts.utils.parser_helper import sanitize_template, get_value
from utils import get_text
from scripts.match2conversion.external_links import MATCH_LINKS, MAP_LINKS

ALL_LINKS = MATCH_LINKS + MAP_LINKS
def write_map(key, value):
	return '\n\t|'+ key + '=' + value

def add_to_list(_list, name, value):
	if value:
		_list.append(name + value)

def process_old(text: str):
	links = []
	comments = []
	matchCounter = 0
	wikicode = mwparserfromhell.parse(text)
	for template in wikicode.filter_templates(matches=lambda n: str(n.name).strip() == "BracketMatchSummary"):
		matchCounter = matchCounter + 1
		template = sanitize_template(template)
		for parameter in template.params:
			name = str(parameter.name)
			if name in ALL_LINKS:
				add_to_list(links, name, get_value(template, name))
			name = name[:-1]
			if name in ALL_LINKS:
				add_to_list(links, name, get_value(template, name))
			if name == 'comment':
				val = get_value(template, name)
				if val:
					comments.append(str(matchCounter) + val)

	return links, comments

def process_new(text: str):
	links = []
	comments = []
	matchCounter = 0
	wikicode = mwparserfromhell.parse(text)
	for template in wikicode.filter_templates(matches=lambda n: str(n.name).strip() == "Match"):
		matchCounter = matchCounter + 1
		template = sanitize_template(template)
		for parameter in template.params:
			name = str(parameter.name)
			if name in ALL_LINKS:
				add_to_list(links, name, get_value(template, name))
			if name == 'comment':
				val = get_value(template, name)
				if val:
					comments.append(str(matchCounter) + val)

	for template in wikicode.filter_templates(matches=lambda n: str(n.name).strip() == "Map"):
		template = sanitize_template(template)
		for parameter in template.params:
			name = str(parameter.name)
			if name in MAP_LINKS:
				add_to_list(links, name, get_value(template, name))

	return links, comments

def main(*args):
	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	#skip 2000
	skip_number = 0
	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue
		option, _, value = arg.partition(':')
		if option == '-skip':
			skip_number = int(value or pywikibot.input(
				'How many files do you want to skip?'))


	generator = genFactory.getCombinedGenerator()
	index = 0
	for page in generator:
		if index < skip_number:
			index = index + 1
			continue
		index = index + 1
		print(str(page))
		revisions = page.revisions(content=False, total = 25)
		revisions = list(revisions)
		revId = ''
		next = False
		for revision in revisions:
			if revision.comment:
				if 'Convert' in revision.comment:
					revId = revision.revid
					next = True
					continue
			if next:
				revId = revision.revid
				next = False
		if revId != '':
			oldLinks, oldComments = process_old(page.getOldVersion(oldid = revId))
			if len(oldLinks) > 0 or len(oldComments) > 0:
				code = ''
				newLinks, newComments = process_new(get_text(page))
				if sorted(oldLinks) != sorted(newLinks):
					code = 'link'
				if sorted(oldComments) != sorted(newComments):
					code = code + 'comment'
				if code:
					with open("recheck_page.txt", "a", encoding = 'utf-8') as f:
						f.write("*" + code + ".." + str(page) + "\n")

		if index % 250 == 0:
			print("index -------" + str(index) + "\n")
if __name__ == '__main__':
	main()