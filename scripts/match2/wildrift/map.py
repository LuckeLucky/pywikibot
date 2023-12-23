from ..commons.utils import getValueOrEmpty, PrefixIterator
from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def getPrefixedParams(self, prefix: str) -> str:
		result = ""
		for key in PrefixIterator(prefix, self.data):
			result += f"|{key}={self.data[key]}"
		return result

	def __str__(self) -> str:
		indent = "    "
		out = "{{Map\n"
		vod = getValueOrEmpty(self.data, 'vod')
		if vod:
			out += out + f"|vod={vod}"
		out += (
			f"{indent}|team1side={getValueOrEmpty(self.data, 'team1side')}" +
			f"|team2side={getValueOrEmpty(self.data, 'team2side')}" +
			f"|length={getValueOrEmpty(self.data, 'length')}"
			f"|winner={getValueOrEmpty(self.data, 'win')}\n"
		)

		team1picks = self.getPrefixedParams('t1c')
		if team1picks:
			out += indent + "<!-- Champion/Hero picks -->\n"
			out += f"{indent}{team1picks}\n"
		team2picks = self.getPrefixedParams('t2c')
		if team2picks:
			out += f"{indent}{team2picks}\n"

		team1bans = self.getPrefixedParams('t1b')
		if team1bans:
			out += indent + "<!-- Champion/Hero bans -->\n"
			out += f"{indent}{team1bans}\n"
		team2bans = self.getPrefixedParams('t2b')
		if team2bans:
			out += f"{indent}{team2bans}\n"

		out += indent + "}}"
		return out
