import re
from typing import Dict, Generator, List, Self

from mwparserfromhell.nodes import Template as mwTemplate

class Template:
	def __init__(self) -> None:
		self._name: str = ''
		self._data: Dict[str, str|Template] = {}

	@classmethod
	def initFromTemplate(cls, template: mwTemplate, removeComments: bool = False) -> Self:
		self = cls()
		self._name = template.name.strip()
		for parameter in template.params:
			name = str(parameter.name).strip()
			value = str(parameter.value)
			if '<!--' in value and removeComments:
				value = re.sub(r'(<!--.*?-->)', '', value, 0, re.MULTILINE)
			value = value.strip()
			if value.startswith('{{'):
				self._data[name] = Template.initFromTemplate(parameter.value.filter_templates(recursive=False)[0], removeComments)
			else:
				self._data[name] = value
		return self

	@classmethod
	def initFromDict(cls, name: str, data: dict) -> Self:
		self = cls()
		self._name = name
		self._data = data
		return self

	@classmethod
	def createFakeTemplate(cls) -> Self:
		self = cls()
		self._name = 'FAKE'
		self._data = {}
		return self

	def has(self, key: str) -> bool:
		return key in self._data

	def add(self, key: str, value: str|Self) -> None:
		self._data[key] = value

	def get(self, key: str) -> str | Self:
		return self._data[key] if key in self._data else ''

	def remove(self, key: str) -> None:
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

	def getNestedTemplate(self, name: str, index: int = 0) -> Self:
		key = name + (str(index) if index > 0  else '')
		return self._data[key] if key in self._data else None


	def iterateParams(self, nested: bool = False) -> Generator[tuple[str, str | Self], None, None]:
		for key, value in self._data.items():
			if isinstance(value, Template) and nested:
				value.iterateParams(nested)
			else:
				yield key, value

	def iterateByPrefix(self, prefix: str, ignoreEmpty: bool = False) -> Generator[tuple[str, str | Self], None, None]:
		for key, value in self._data.items():
			if key.startswith(prefix):
				if ignoreEmpty and not value:
					continue
				yield key, value

	def iterateByItemsMatch(self, items: List[str], ignoreEmpty: bool = False) -> Generator[tuple[str, str | Self], None, None]:
		for item in items:
			if item in self._data:
				val = self._data[item]
				if ignoreEmpty and not val:
					continue
				yield item, val
