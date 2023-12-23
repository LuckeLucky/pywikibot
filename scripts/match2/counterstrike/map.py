from mwparserfromhell.nodes import Template
from ..commons.template import Template
from ..commons.map import Map as commonsMap

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

class Map(commonsMap):
	def __init__(self, index: int, template: Template) -> None:
		super().__init__(index, template)
		self.prefix = 'map' + str(self.index)
		winner = self.template.getValue(self.prefix + 'win')
		if winner in ['1', '2', '0']:
			self.winner = int(winner)
			self.finished = 'true'
		elif winner == 'draw':
			self.winner = 0
			self.finished = 'true'
		elif winner == SKIP:
			self.finished = SKIP
		score = self.template.getValue(self.prefix + 'score')
		self.score = score.split('-', 1)
		strIndex = str(self.index)
		self.links = [x + strIndex for x in MAP_LINKS]

	def getHalfScores(self, halfKey: str) -> str:
		result = ""
		halfKey = self.prefix + halfKey
		for key in [halfKey + 't1firstside', halfKey + 't1t', halfKey + 't1ct', halfKey + 't2t', halfKey + 't2ct']:
			val = self.template.getValue(key)
			if val:
				result += f"|{key.replace(self.prefix, '')}={val}"
		return result

	def __str__(self) -> str:
		indent = "\t"
		out = f"{{{{Map|map={self.template.getValue(self.prefix)}"

		if len(self.score) == 2:
			out += f"|score1={self.score[0]}|score2={self.score[1]}"
		out += f"|finished={self.finished}"

		if self.finished == SKIP:
			out += '}}'
			return out
		out += "\n"

		halfKey = ''
		overtimes = 0
		while True:
			half = self.getHalfScores(halfKey)
			if half:
				out += f"{indent}{half}\n"
				overtimes += 1
				halfKey = 'o' + str(overtimes)
			else:
				break

		if halfKey == '':
			out += f"{indent}|winner={self.winner}\n"

		for key, value in self.template.iterateByItemsMatch(self.links):
			suffix = key.removesuffix(str(self.index))
			out += f"{indent}|{suffix}={value}"

		vod = self.template.getValue('vodgame' + str(self.index))
		if vod:
			out += f"\n|vod={vod}"
		vod2 = self.template.getValue('2vodgame' + str(self.index))
		if vod2:
			out += f"\n|vod2={vod2}"

		out += "\n" + indent + "}}"
		return out
