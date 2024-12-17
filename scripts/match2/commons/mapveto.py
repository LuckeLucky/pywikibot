from typing import List

from .template import Template
from .templateutils import TemplateUtils

DECIDER = 'decider'

class MapVeto(TemplateUtils):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'MapVeto\n    ', indent = '    ', end = '}}')

	def __init__(self, template: Template) -> None:
		super().__init__(template)

	def __str__(self) -> str:
		out = [
			('firstpick', self.getValue('firstban'), True)
		]

		vetoTypes = []
		vetos = []
		decider = ''
		for key, value in self.template.iterateByPrefix('r'):
			vetoIndex = key.replace('r', '')
			vetoTypes.append(value)
			if value == DECIDER:
				decider = self.getValue('map' + vetoIndex)
			else:
				t1Veto = f't1map{vetoIndex}'
				t2Veto = f't2map{vetoIndex}'
				vetos.append([
					(t1Veto, self.getValue(t1Veto)),
					(t2Veto, self.getValue(t2Veto))
				])
			out.extend(vetos)

		if len(vetoTypes) > 0:
			out.append(('types', vetoTypes))

		out.append(('decider', decider, True))

		return self.generateString(out)
