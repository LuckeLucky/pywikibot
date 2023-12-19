import re
import random
import string

from mwparserfromhell.nodes import Template

class PrefixIterator:
	def __init__(self, prefix: str, dictionary: dict):
		self.keys = [key for key in dictionary if key.startswith(prefix)]
		self.index = 0

	def __iter__(self):
		return self

	def __next__(self):
		if self.index < len(self.keys):
			currentKey = self.keys[self.index]
			self.index += 1
			return currentKey
		raise StopIteration

class KeysInDictionaryIterator:
	def __init__(self, keys: list, dictionary: dict) -> None:
		self.keys = []
		for key in keys:
			if key in dictionary:
				self.keys.append(key)
		self.index = 0
	def __iter__(self):
		return self

	def __next__(self):
		if self.index < len(self.keys):
			currentKey = self.keys[self.index]
			self.index += 1
			return currentKey
		raise StopIteration

def getValueOrEmpty(dictionary: dict, key: str):
	if key in dictionary:
		return dictionary[key]
	else:
		return ""

def sanitizeTemplate(template: Template, removeComments: bool = False):
	if template is None:
		return template
	for parameter in template.params:
		name = str(parameter.name)
		value = str(parameter.value).strip()
		if '<!--' in value and removeComments:
			value = re.sub(r'(<!--.*?-->)', '', value, 0, re.MULTILINE)
		template.add(name, value.strip(), preserve_spacing=False)
	return template

def getStringFromTemplate(template: Template, key: str = None, index: int = -1) -> str:
	'''Check if template has a key, if true return str(value) or None'''
	if template is None:
		return None
	if key:
		if template.has(key):
			return str(template.get(key).value)
	if index >= 0:
		if len(template.params) > index:
			return str(template.params[index].value)
	return None

def getNestedTemplateFromTemplate(template: Template, key: str) -> Template:
	if template is None:
		return None
	if template.has(key):
		return template.get(key).value.filter_templates()[0]
	return None

def generateId():
	ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
	return ran

def getTemplateParameters(template: Template) -> dict:
	if template is None:
		return {}
	data = {}
	for parameter in template.params:
		key = str(parameter.name)
		data[key] = str(parameter.value)
	return data
