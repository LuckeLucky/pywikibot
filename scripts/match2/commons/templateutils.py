from typing import List
from .template import Template

class TemplateUtils:
	def __init__(self, template: Template) -> None:
		self.template = template
		if not self.template:
			self.template = Template.createFakeTemplate()

	def getValue(self, name: str) -> str:
		return self.template.getValue(name)

	def printParam(self, paramName: str, newParamName: str = '', end: str = '', ignoreIfEmpty: bool = False) -> str:
		value = self.template.getValue(paramName)
		if ignoreIfEmpty and not value:
			return ''
		if newParamName:
			paramName = newParamName
		return f'|{paramName}={value}' + end

	def printPrefixed(self, prefix: str, separator: str = '', end: str = '', ignoreIfResultEmpty: bool = False) -> str:
		result = []
		for key, value in self.template.iterateByPrefix(prefix):
			result.append(f'|{key}={value}')

		if not result and ignoreIfResultEmpty:
			return ''

		return separator.join(result) + end

	def printMatch(self, matches: List[str], end: str = '', ignoreIfResultEmpty: bool = False) -> str:
		result = []
		for key, value in self.template.iterateByItemsMatch(matches):
			result.append(f'|{key}={value}')

		if not result and ignoreIfResultEmpty:
			return ''

		return ''.join(result) + end

	def printTemplate(self, params: List[str], templateId: str, indent: str, end: str = '}}', ignoreEmptyParams: bool = False) -> str:
		params = [indent + item for item in params if item]
		result = ''
		for item in params:
			if not item and ignoreEmptyParams:
				continue
			result += item

		return '{{' + templateId + '\n' + result + end
