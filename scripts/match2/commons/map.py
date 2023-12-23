from .template import Template

class Map:
	def __init__(self, index: int, template: Template) -> None:
		self.index = index
		self.template = template
		if not self.template:
			self.template = Template.createFakeTemplate()
