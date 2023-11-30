from mwparserfromhell.nodes import Template

from ..utils import *
from ..map import Map

class Map(Map):
	def __init__(self, index: int, template: Template) -> None:
		super().__init__(index, template)

	def __str__(self) -> str:
		indent = "  "
		out = ("{{Map\n" +
			f"{indent}|team1side={get_value_or_empty(self.data, 'team1side')}\n"
		)

		team1picks = ""
		for key in PrefixIterator('t1c', self.data):
			team1picks += f"|{key}={self.data[key]}"
		if team1picks:
			out += f"{indent}{team1picks}\n"

		out = out + f"{indent}|team2side={get_value_or_empty(self.data, 'team2side')}\n"

		team2picks = ""
		for key in PrefixIterator('t2c', self.data):
			team2picks += f"|{key}={self.data[key]}"
		if team2picks:
			out += f"{indent}{team2picks}\n"

		out += f"{indent}|length={get_value_or_empty(self.data, 'length')}"
		out += f" |winner={get_value_or_empty(self.data, 'win')}"

		out += "\n" + indent + "}}"
		return out