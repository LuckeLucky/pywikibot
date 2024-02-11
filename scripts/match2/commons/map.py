from .template import Template

class Map:
	def __init__(self, index: int, template: Template) -> None:
		self.indent = '        '
		self.index = index
		self.prefix = 'map' + str(self.index)
		self.template = template
		if not self.template:
			self.template = Template.createFakeTemplate()
