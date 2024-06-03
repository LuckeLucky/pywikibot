from .template import Template

class TemplateUtils:
	def __init__(self, template: Template) -> None:
		self.template = template
		if not self.template:
			self.template = Template.createFakeTemplate()

	def getValue(self, name: str) -> str:
		return self.template.getValue(name)

	def printParam(self, paramName: str, newParamName: str = '') -> str:
		value = self.template.getValue(paramName)
		if newParamName:
			paramName = newParamName
		return f'|{paramName}={value}'
