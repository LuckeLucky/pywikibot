from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def getPrefixedParams(self, prefix: str) -> str:
		result = ""
		for key, value in self.template.iterateByPrefix(prefix):
			result += f"|{key}={value}"
		return result

	def __str__(self) -> str:
		indent = self.indent
		out = '{{Map'
		vod = self.template.getValue('vod')
		if vod:
			out += f'|vod={vod}'
		out = out + "\n"
		out = (
			out +
			f"{indent}|team1side={self.template.getValue('team1side')}" +
			f"|team2side={self.template.getValue('team2side')}" +
			f"|length={self.template.getValue('length')}"
			f"|winner={self.template.getValue('win')}\n"
		)

		team1picks = self.getPrefixedParams('t1h')
		team2picks = self.getPrefixedParams('t2h')
		if team1picks:
			out += f'{indent}<!-- Hero picks -->\n'
			out += f"{indent}{team1picks}\n"
		if team2picks:
			out += f"{indent}{team2picks}\n"

		team1bans = self.getPrefixedParams('t1b')
		team2bans = self.getPrefixedParams('t2b')
		if team1bans:
			out += f'{indent}<!-- Hero bans -->\n'
			out += f"{indent}{team1bans}\n"
		if team2bans:
			out += f"{indent}{team2bans}\n"

		out += indent[:len(indent)//2] + "}}"
		return out
