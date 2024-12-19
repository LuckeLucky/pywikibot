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
		winner = self.getValue(self.prefix + 'win')
		if winner in ['1', '2', '0', 'draw']:
			self.winner = 0 if winner == 'draw' else int(winner)
			self.finished = 'true'
		elif winner == SKIP:
			self.winner = ''
			self.finished = SKIP
		else:
			self.winner = ''
			self.finished = ''
		score = self.getValue(self.prefix + 'score')
		self.score = score.split('-', 1)
		strIndex = str(self.index)
		self.links = [x + strIndex for x in MAP_LINKS]

	def getHalfScores(self, halfKey: str) -> list:
		result = []
		halfKey = self.prefix + halfKey
		for key in [halfKey + 't1firstside', halfKey + 't1t', halfKey + 't1ct', halfKey + 't2t', halfKey + 't2ct']:
			val = self.getValue(key)
			if val:
				result.append((key.replace(self.prefix, ''), val))
		return result

	def __str__(self) -> str:
		out = [
			[('map', self.getValue(self.prefix)), ('finished', self.finished)],
		]
		if self.finished == SKIP:
			return self.generateString(out)

		if len(self.score) == 2:
			out.append([('score1', self.score[0]), ('score2', self.score[1])])

		halfKey = ''
		overtimes = 0
		while True:
			half = self.getHalfScores(halfKey)
			if len(half) > 0:
				out.append(half)
				overtimes += 1
				halfKey = 'o' + str(overtimes)
			else:
				break

		if halfKey == '':
			out.append(('winner', self.winner))

		links = []
		for key, value in self.template.iterateByItemsMatch(self.links):
			suffix = key.removesuffix(str(self.index))
			links.append((suffix, value))
		links.append(('vod', self.getValue('vodgame' + str(self.index)), True))
		links.append(('vod2', self.getValue('2vodgame' + str(self.index)), True))

		out.append(links)

		return self.generateString(out)
