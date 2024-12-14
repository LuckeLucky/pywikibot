from typing import List
from .template import Template

class TemplateUtils:
	def __init__(self, template: Template) -> None:
		self.template = template
		if not self.template:
			self.template = Template.createFakeTemplate()

	def getValue(self, name: str) -> str:
		return self.template.get(name)

	def printParam(self, paramName: str, newParamName: str = '', start: str = '', end: str = '', ignoreIfEmpty: bool = False) -> str:
		value = self.getValue(paramName)
		if ignoreIfEmpty and not value:
			return ''
		if newParamName:
			paramName = newParamName
		return f'{start}|{paramName}={value}' + end
	
	def getFoundMatches(self, matches: List[str]) -> List:
		result = []
		for key, value in self.template.iterateByItemsMatch(matches):
			result.append((key, value))
		return result
	
	def getFoundPrefix(self, prefix: str) -> List:
		result = []
		for key, value in self.template.iterateByPrefix(prefix):
			result.append((key, value))
		return result

	def printPrefixed(self, prefix: str, separator: str = '', end: str = '', ignoreIfResultEmpty: bool = False) -> str:
		result = []
		for key, value in self.template.iterateByPrefix(prefix):
			result.append(f'|{key}={value}')

		if not result and ignoreIfResultEmpty:
			return ''

		return separator.join(result) + end
	
	def formatTulpe(self, param: tuple) -> str|None:
		if len(param) == 3 and param[2] and param[1] == '':
			return None
		return f'|{param[0]}={param[1]}'
	
	def formatNestedList(self, params: List[str]) -> List:
		out = []
		for param in params:
			if type(param) == tuple:
				out.append(self.formatTulpe(param))
		out = [x for x in out if x is not None]
		return ''.join(out) if len(out) > 0 else None
	
	def formatList(self, appendTo: List, params: List[str]) -> List:
		for param in params:
			if type(param) == tuple:
				appendTo.append(self.formatTulpe(param))
			elif type(param) == list:
				appendTo.append(self.formatNestedList(param))
	
		return appendTo

	def generateTemplateString(self, params: List[str], templateId: str, indent: str, end: str = '}}') -> str:
		"""
		params each index is a line, each tulpe is a parameter (key, value, ignoreEmpty)
		"""
		out = self.formatList([], params)
		if len(out) == 1:
			return '{{' + templateId + indent.join(out) + end

		out = [x + '\n' for x in out if x is not None]

		return '{{' + templateId + indent.join(out) + end
