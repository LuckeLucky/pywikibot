
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
	hltvs = 0
	wikicode = mwparserfromhell.parse(text)
	for template in wikicode.filter_templates(matches=lambda n: "bracketmatchsummary" in str(n.name).strip().lower()):
		template = sanitize_template(template)
		for parameter in template.params:
			name = str(parameter.name)
			if name in ALL_LINKS:
				add_to_list(links, name, get_value(template, name))
			splitName = name[:-1]
			if splitName in ALL_LINKS:
				add_to_list(links, splitName, get_value(template, name))
			if name == 'comment':
				val = get_value(template, name)
				if val:
					comments.append(val)
			if 'hltv' in name:
				val = get_value(template, name)
				if val:
					hltvs = hltvs + 1

	return links, comments, hltvs

def process_new(text: str):
	links = []
	comments = []
	hltvs = 0
	wikicode = mwparserfromhell.parse(text)
	for template in wikicode.filter_templates(matches=lambda n: str(n.name).strip() == "Match"):
		template = sanitize_template(template)
		for parameter in template.params:
			name = str(parameter.name)
			if name in ALL_LINKS:
				add_to_list(links, name, get_value(template, name))
			if name == 'comment':
				val = get_value(template, name)
				if val:
					comments.append(val)
			if 'hltv' in name:
				val = get_value(template, name)
				if val:
					hltvs = hltvs + 1

	for template in wikicode.filter_templates(matches=lambda n: str(n.name).strip() == "Map"):
		template = sanitize_template(template)
		for parameter in template.params:
			name = str(parameter.name)
			if name in MAP_LINKS:
				add_to_list(links, name, get_value(template, name))

	return links, comments, hltvs

def main(*args):
	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	#skip 2000
	skip_number = 0
	diff = False
	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue
		option, _, value = arg.partition(':')
		if option == '-skip':
			skip_number = int(value or pywikibot.input(
				'How many files do you want to skip?'))
		if option == '-diff':
			diff = True
		if option == '-hltv':
			ALL_LINKS.extend(['hltv', 'hltv2'])


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
			oldLinks, oldComments, oldHLTVCount = process_old(page.getOldVersion(oldid = revId))
			if len(oldLinks) > 0 or len(oldComments) > 0 or oldHLTVCount > 0:
				newLinks, newComments, newHLTVCount = process_new(get_text(page))
				if not diff:
					code = ''
					if sorted(oldLinks) != sorted(newLinks):
						code = 'link'
					if sorted(oldComments) != sorted(newComments):
						code = code + 'comment'
					if oldHLTVCount != newHLTVCount:
						code = code + 'hltv'
					if code:
						with open("recheck_page.txt", "a", encoding = 'utf-8') as f:
							f.write("*" + code + ".." + str(page) + "\n")
				else:
					print(list(set(oldLinks) - set(newLinks)))
					print(list(set(oldComments) - set(newComments)))

		if index % 250 == 0:
			return
			with open("recheck_page.txt", "a", encoding = 'utf-8') as f:
				f.write("***" + str(index) + "***\n")
if __name__ == '__main__':
	main()