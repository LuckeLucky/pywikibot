from typing import List, Any

import re
from mwparserfromhell.nodes import Template as mwTemplate
from mwparserfromhell.nodes.extras import Parameter

class Template(mwTemplate):
	@staticmethod
	def createFakeTemplate():
		return Template(mwTemplate("FAKE"))

	def __init__(self, template: mwTemplate, removeComments: bool = False):
		params = []
		parameter: Parameter
		for parameter in template.params:
			value = str(parameter.value)
			if '<!--' in value and removeComments:
				value = re.sub(r'(<!--.*?-->)', '', value, 0, re.MULTILINE)
			params.append(Parameter(str(parameter.name).strip(), value.strip(), parameter.showkey))

		super().__init__(template.name.strip(), params)

	def addIfNotHas(self, name: str, value: Any):
		if not self.has(name):
			self.add(name, value)

	def getValue(self, name: str) -> str:
		param: Parameter = None
		if name:
			param = self.get(name, None)
		if param:
			return str(param.value)
		return ''

	def getBool(self, name: str) -> bool:
		val = self.getValue(name)
		if val:
			if val in ['true', 't', 'yes', 'y', '1']:
				return True
		return False

	def getfirstValueFound(self, names: List[str]) -> str:
		for name in names:
			val = self.getValue(name)
			if val:
				return val
		return ''

	def getNestedTemplate(self, name: str) -> mwTemplate:
		param: Parameter = self.get(name, None)
		if param:
			templates = param.value.filter_templates()
			return templates[0] if len(templates) > 0 else None
		return None

	def iterateParams(self, nested: bool = False):
		for param in self.params:
			if param.value.startswith('{{') and nested:
				nestedTemplate = Template(self.getNestedTemplate(param.name))
				for _nestedParam in nestedTemplate.params:
					yield str(_nestedParam.name), str(_nestedParam.value)
			else:
				yield str(param.name), str(param.value)

	def iterateByPrefix(self, prefix: str, ignoreEmpty: bool = False):
		for param in self.params:
			if param.name.startswith(prefix):
				if ignoreEmpty and not param.value:
					continue
				yield str(param.name), str(param.value)

	def iterateByItemsMatch(self, items: List[str], ignoreEmpty: bool = False):
		for item in items:
			if self.has(item):
				val = self.getValue(item)
				if ignoreEmpty and not val:
					continue
				yield item, val
