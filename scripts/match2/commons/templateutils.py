from typing import List
from .template import Template

class TemplateUtils:
	def __init__(self, template: Template) -> None:
		self.template: Template = template
		if not self.template:
			self.template = Template.createFakeTemplate()

	def getValue(self, name: str) -> str:
		return self.template.get(name)

	def getFoundMatches(self, matches: List[str]) -> List:
		result = []
		for key, value in self.template.iterateByItemsMatch(matches):
			result.append((key, value))
		return result

	def getFoundPrefix(self, prefix: str, keyMaker = lambda key: key) -> List:
		result = []
		for key, value in self.template.iterateByPrefix(prefix):
			result.append((keyMaker(key), value))
		return result

	def _generateStringFromTuple(self, param: tuple) -> str|None:
		if len(param) == 3 and param[2] and param[1] == '':
			return None
		return f'|{param[0]}={param[1]}'

	def _generateStringFromNestedList(self, params: List[str]) -> List:
		out = []
		for param in params:
			if isinstance(param, tuple):
				out.append(self._generateStringFromTuple(param))
		out = [x for x in out if x is not None]
		return ''.join(out) if len(out) > 0 else None

	def _generateStringFromList(self, appendTo: List, params: List[str]) -> List:
		for param in params:
			if isinstance(param, tuple):
				appendTo.append(self._generateStringFromTuple(param))
			elif isinstance(param, list):
				appendTo.append(self._generateStringFromNestedList(param))
		return appendTo

	def generateTemplateString(self, params: List[str], templateId: str, indent: str, end: str = '}}') -> str:
		"""
		params each index is a line, each tulpe is a parameter (key, value, ignoreEmpty)
		"""
		out = self._generateStringFromList([], params)
		if len(out) == 1:
			return '{{' + templateId + indent.join(out) + end

		out = [x + '\n' for x in out if x is not None]

		return '{{' + templateId + indent.join(out) + end