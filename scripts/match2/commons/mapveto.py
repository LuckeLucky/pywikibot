from .template import Template

DECIDER = 'decider'

class MapVeto:
	def __init__(self, template: Template) -> None:
		self.indent = '  '
		self.template = template

	def __str__(self) -> str:
		out = '{{MapVeto\n'
		fp = self.template.getValue('firstban')
		if fp:
			out += self.indent + f'|firstpick={fp}\n'

		vetoTypes = []
		vetos = []
		decider = ''
		for key, value in self.template.iterateByPrefix('r'):
			vetoIndex = key.replace('r', '')
			vetoTypes.append(value)
			if value == DECIDER:
				decider = self.template.getValue('map' + vetoIndex)
			else:
				t1Veto = f't1map{vetoIndex}'
				t2Veto = f't2map{vetoIndex}'
				vetos.append((f'|{t1Veto}={self.template.getValue(t1Veto)}',
					f'|{t2Veto}={self.template.getValue(t2Veto)}'))

		if len(vetoTypes) > 0:
			out += self.indent + '|types=' + ','.join(vetoTypes) + '\n'

		for t1Veto, t2Veto in vetos:
			out += self.indent + t1Veto + ' ' + t2Veto + '\n'

		if decider:
			out += self.indent + f'|decider={decider}\n'

		out += '}}'
		return out
