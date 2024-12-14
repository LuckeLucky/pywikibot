from typing import List, Dict

import re
import mwparserfromhell.nodes as mwnodes
from mwparserfromhell.nodes import Template as mwTemplate
from mwparserfromhell.nodes.extras import Parameter

class Template:
	def __init__(self):
		self._name: str = ''
		self._data: Dict[str, str|Template] = {}

	@classmethod
	def initFromTemplate(cls, template: mwTemplate, removeComments: bool = False):
		self = cls()
		self._name = template.name.strip()
		for parameter in template.params:
			name = str(parameter.name).strip()
			value = parameter.value
			for node in value.nodes:
				index = 0
				if type(node) == mwnodes.text.Text:
					value = str(parameter.value)
					if '<!--' in value and removeComments:
						value = re.sub(r'(<!--.*?-->)', '', value, 0, re.MULTILINE)
					self._data[name] = value.strip()
				elif type(node) == mwnodes.Template:
					self._data[name if index == 0 else name + str(index)] = Template.initFromTemplate(node, removeComments)
					index += 1
		return self
	
	@classmethod
	def initFromDict(cls, name: str, data: dict):
		self = cls()
		self._name = name
		self._data = data
		return self
	
	@classmethod
	def createFakeTemplate(cls):
		self = cls()
		self._name = 'FAKE'
		self._data = {}
		return self
	
	def has(self, key: str) -> bool:
		return key in self._data
	
	def add(self, key, value):
		self._data[key] = value

	def get(self, key: str):
		return self._data[key] if key in self._data else ''

	def remove(self, key):
		del self._data[key]

	def getBool(self, name: str) -> bool:
		val = self.get(name)
		if val:
			if val in ['true', 't', 'yes', 'y', '1']:
				return True
		return False

	def getfirstValueFound(self, names: List[str]) -> str:
		for name in names:
			val = self.get(name)
			if val:
				return val
		return ''

	def getNestedTemplate(self, name: str, index: int = 0) -> mwTemplate:
		key = name + (str(index) if index > 0  else '')
		return self._data[key] if key in self._data else None


	def iterateParams(self, nested: bool = False):
		for key, value in self._data.items():
			if type(value) == Template:
				Template.iterateParams(value, nested)
			else:
				yield key, value

	def iterateByPrefix(self, prefix: str, ignoreEmpty: bool = False):
		for key, value in self._data.items():
			if key.startswith(prefix):
				if ignoreEmpty and not value:
					continue
				yield key, value

	def iterateByItemsMatch(self, items: List[str], ignoreEmpty: bool = False):
		for item in items:
			if item in self._data:
				val = self._data[item]
				if ignoreEmpty and not val:
					continue
				yield item, val
