from mwparserfromhell.nodes import Template
from ..commons.utils import Template
from ..commons.map import Map
from ..commons.utils import *

MAP_LINKS = [
	'esl',
	'esea',
	'faceit',
	'esportal',
	'sostronk',
	'5ewin',
	'5earena',
	'b5csgo',
	'wanmei',
	'challengeme',
	'challengermode',
	'gotfrag',
	'gamersclub',
	'gamersclublobby',
	'coliseum',
	'legacystats',
	'stats',
	'cstats',
]

SKIP = 'skip'

class Map(Map):
	def __init__(self, index: int, template: Template) -> None:
		super().__init__(index, template)
		self.prefix = 'map' + str(self.index)
		winner = get_parameter_str(self.template, self.prefix + 'win')
		if winner in ['1', '2', '0']:
			self.winner = int(winner)
			self.finished = 'true'
		elif winner == 'draw':
			self.winner = 0
			self.finished = 'true'
		elif winner == SKIP:
			self.finished = SKIP
		score = get_parameter_str(self.template, self.prefix + 'score')
		self.score = score.split('-', 1)
		strIndex = str(self.index)
		self.links = [x + strIndex for x in MAP_LINKS]

	def get_half(self, half: str) -> str:
		result = ""
		for key in [half + 't1firstside', half + 't1t', half + 't1ct', half + 't2t', half + 't2ct']:
			val = self.data[key]
			if val:
				result += f"|{key}={val}"
		return result

	def __str__(self) -> str:
		indent = "\t"
		out = f"{{{{Map|map={get_value_or_empty(self.data, self.prefix)}"

		if len(self.score) == 2:
			out += f"|score1={self.score[0]}|score2={self.score[1]}"
		out += f"|finished={self.finished}"

		if self.finished == SKIP:
			out += '}}'
			return out
		out += "\n"

		out += f"{indent}|winner={self.winner}\n"

		while(True):
			halfKey = ''
			overtimes = 0
			half = self.get_half(halfKey)
			if half:
				out += f"{indent}{half}\n"
			else:
				break
			overtimes += 1
			halfKey = 'o' + str(overtimes)

		for key in KeysInDictionaryIterator(self.links, self.data):
			out += f"|{key}={self.data[key]}"
		
		vod = get_value_or_empty(self.data, 'vodgame' + str(self.index))
		if vod:
			out += f"\n|vod={vod}"
		vod2 = get_value_or_empty(self.data, '2vodgame' + str(self.index))
		if vod2:
			out += f"\n|vod2={vod2}"

		out += "\n" + indent + "}}"
		return out