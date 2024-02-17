from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def getPrefixedParams(self, prefix: str) -> str:
		result = ""
		for key, value in self.template.iterateByPrefix(prefix):
			result += f"|{key}={value}"
		return result

	def __str__(self) -> str:
		out = ("{{Map\n" +
			f"|team1side={self.template.getValue('team1side')}\n"
		)

		team1picks = self.getPrefixedParams('t1h')
		if team1picks:
			out += f"{team1picks}\n"
		team1bans = self.getPrefixedParams('t1b')
		if team1bans:
			out += f"{team1bans}\n"

		out = out + f"|team2side={self.template.getValue('team2side')}\n"

		team2picks = self.getPrefixedParams('t2h')
		if team2picks:
			out += f"{team2picks}\n"
		team2bans = self.getPrefixedParams('t2b')
		if team2bans:
			out += f"{team2bans}\n"

		out += f"|length={self.template.getValue('length')}"
		out += f"|winner={self.template.getValue('win')}\n"

		out += "}}"
		return out
