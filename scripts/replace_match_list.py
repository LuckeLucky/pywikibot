import pywikibot
import mwparserfromhell
import random
import string

from pywikibot import pagegenerators
from mwparserfromhell.nodes import Template
from mwparserfromhell.nodes.extras import Parameter
from utils import get_text, put_text

def generate_id():
	ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
	return ran

def create_new_template(oldTemplate: Template, new_template_name: str):
	new_template = Template(new_template_name, oldTemplate.params)
	param = Parameter('id', generate_id())
	new_template.params.insert(0, param)
	return new_template

def process_match_list(text: str, old_template_name: str, new_template_name: str):
	wikicode = mwparserfromhell.parse(text)
	for template in wikicode.filter_templates():
		if template.name.matches(old_template_name):
			new_template = create_new_template(template, new_template_name)
			wikicode.replace(template, new_template)

	return str(wikicode)

def main(*args):
	# summary message
	edit_summary = 'Convert old MatchList to Legacy Version'

	# Read commandline parameters.
	local_args = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()

	old_template_name = ''
	new_template_name = ''

	for arg in local_args:
		if genFactory.handle_arg(arg):
			continue
		if arg.startswith('-'):
			arg = arg[1:]
			arg, _, value = arg.partition(':')
			if arg == 'oldTemplate':
				old_template_name = value
			if arg == 'newTemplate':
				new_template_name = value
	
	if not old_template_name:
		old_template_name = pywikibot.input('Old template name:')

	if not new_template_name:
		new_template_name = pywikibot.input('New template name:')
			
	generator = genFactory.getCombinedGenerator()
	for page in generator:
		if not page.has_permission():
			continue
		text = get_text(page)
		new_text = process_match_list(text, old_template_name, new_template_name)
		put_text(page, summary=edit_summary, new=new_text)

if __name__ == '__main__':
	main()