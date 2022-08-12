from mwparserfromhell.nodes import Template

import random
import string

def generate_id():
	ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
	return ran


def sanitize_template(template: Template):
	for parameter in template.params:
		value = str(parameter.value)
		template.add(str(parameter.name), value.rstrip(), preserve_spacing=False)

