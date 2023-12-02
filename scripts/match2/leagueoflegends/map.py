from mwparserfromhell.nodes import Template

from ..utils import *
from ..map import Map

class Map(Map):
	def get_team_params(self, prefix: str) -> str:
		result = ""
		for key in PrefixIterator(prefix, self.data):
			result += f"|{key}={self.data[key]}"
		return result

	def __str__(self) -> str:
		indent = "  "
		out = ("{{Map\n" +
			f"{indent}|team1side={get_value_or_empty(self.data, 'team1side')}\n"
		)

		team1picks = self.get_team_params('t1c')
		if team1picks:
			out += f"{indent}{team1picks}\n"
		team1bans = self.get_team_params('t1b')
		if team1bans:
			out += f"{indent}{team1bans}\n"

		out = out + f"{indent}|team2side={get_value_or_empty(self.data, 'team2side')}\n"

		team2picks = self.get_team_params('t2c')
		if team2picks:
			out += f"{indent}{team2picks}\n"
		team2bans = self.get_team_params('t2b')
		if team2bans:
			out += f"{indent}{team2bans}\n"

		out += f"{indent}|length={get_value_or_empty(self.data, 'length')}"
		out += f" |winner={get_value_or_empty(self.data, 'win')}"

		out += "\n" + indent + "}}"
		return out