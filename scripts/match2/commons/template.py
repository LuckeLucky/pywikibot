from typing import List

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

	def getValue(self, key: str = '', index: int = -1) -> str:
		param: Parameter = None
		if key:
			param = self.get(key, None)
		elif 0 <= index < len(self.params):
			param = self.params[index]

		if param:
			return str(param.value)
		return ''

	def getNestedTemplate(self, key: str) -> mwTemplate:
		param: Parameter = self.get(key, None)
		if param:
			return param.value.filter_templates()[0]
		return None

	def iterateParams(self, nested: bool = False):
		for param in self.params:
			if param.value.startswith('{{') and nested:
				nestedTemplate = Template(self.getNestedTemplate(param.name))
				for _nestedParam in nestedTemplate.params:
					yield _nestedParam.name, _nestedParam.value
			else:
				yield param.name, param.value

	def iterateByPrefix(self, prefix: str, ignoreEmpty: bool = False):
		for param in self.params:
			if param.name.startswith(prefix):
				if ignoreEmpty and not param.value:
					continue
				yield param.name, param.value

	def iterateByItemsMatch(self, items: List[str], ignoreEmpty: bool = False):
		for item in items:
			if self.has(item):
				val = self.getValue(item)
				if ignoreEmpty and not val:
					continue
				yield item, val
