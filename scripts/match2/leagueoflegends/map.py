from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def getPrefixedParams(self, prefix: str) -> str:
		result = ""
		for key, value in self.template.iterateByPrefix(prefix):
			result += f"|{key}={value}"
		return result

	def __str__(self) -> str:
		indent = self.indent
		out = ("{{Map\n" +
			f"{indent}|team1side={self.template.getValue('team1side')}\n"
		)

		team1picks = self.getPrefixedParams('t1c')
		if team1picks:
			out += f"{indent}{team1picks}\n"
		team1bans = self.getPrefixedParams('t1b')
		if team1bans:
			out += f"{indent}{team1bans}\n"

		out = out + f"{indent}|team2side={self.template.getValue('team2side')}\n"

		team2picks = self.getPrefixedParams('t2c')
		if team2picks:
			out += f"{indent}{team2picks}\n"
		team2bans = self.getPrefixedParams('t2b')
		if team2bans:
			out += f"{indent}{team2bans}\n"

		out += f"{indent}|length={self.template.getValue('length')}"
		out += f" |winner={self.template.getValue('win')}\n"

		out += indent[:len(indent)//2] + "}}"
		return out
