from typing import Tuple, List
from ..commons.template import Template

from ..commons.map import Map as commonsMap

MAX_NUMBER_OF_OPPONENTS = 2
MAX_NUMBER_OF_PLAYERS = 5

SKIP = 'skip'

class Map(commonsMap):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Map\n        ', indent = '        ', end = '    }}')

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

	def getPlayerStats(self, oppIndex: int, playerIndex: int) -> Tuple[str, bool]:
		teamX = self.prefix + 't' + str(oppIndex)
		pIdx = str(playerIndex)
		player = self.getValue(teamX + 'p' + pIdx)
		agent = self.getValue(teamX + 'a' + pIdx)
		acs = self.getValue(teamX + 'acs' + pIdx)
		kda = self.getValue(teamX + 'kda' + pIdx)
		ok = True
		if (player == '' and
				agent == '' and
				acs == '' and
				kda == ''):
			ok = False

		splitKda = kda.split('/')
		if len(splitKda) == 1:
			splitKda = ['', '', '']
		out = ("{{PSI" +
			f"|player={player}"+
			f"|agent={agent}" +
			f"|kills={splitKda[0]}"
			f"|deaths={splitKda[1]}"
			f"|assists={splitKda[2]}"
			f"|acs={acs}" +
			"}}")
		return out, ok

	def __str__(self) -> str:
		if self.finished == SKIP:
			return self.generateString([
				[('map', self.getValue(self.prefix)), ('finished', self.finished)],
			])

		out = []
		hasOk = False
		for oppIndex in range(1, MAX_NUMBER_OF_OPPONENTS+1):
			for playerIndex in range(1, MAX_NUMBER_OF_PLAYERS+1):
				playerOut, ok = self.getPlayerStats(oppIndex, playerIndex)
				out.append((f't{oppIndex}p{playerIndex}', playerOut, ok))
				hasOk = True if ok or hasOk else False
			if hasOk:
				lastStats = out[-1]
				value = lastStats[1] + '\n'
				out[-1] = (lastStats[0], value)

		hasHalfScores = False
		if self.getValue(self.prefix + 't1firstside'):
			hasHalfScores = True
			out.append([
				('t1firstside', self.getValue(self.prefix + 't1firstside')),
				('t1atk', self.getValue(self.prefix + 't1atk')),
				('t1def', self.getValue(self.prefix + 't1def')),
				('t2atk', self.getValue(self.prefix + 't2atk')),
				('t2def', self.getValue(self.prefix + 't2def'))
			])
		if self.getValue(self.prefix + 'o1t1firstside'):
			out.append([
				('t1firstsideot', self.getValue(self.prefix + 'o1t1firstside')),
				('t1otatk', self.getValue(self.prefix + 'o1t1atk')),
				('t1otdef', self.getValue(self.prefix + 'o1t1def')),
				('t2otatk', self.getValue(self.prefix + 'o1t2atk')),
				('t2otdef', self.getValue(self.prefix + 'o1t2def')),
			])

		if not hasHalfScores and len(self.score) == 2:
			out.append([('score1', self.score[0]), ('score2', self.score[1])])

		out.append([
			('map', self.getValue(self.prefix)),
			('finished', self.finished),
			('length', self.getValue(self.prefix + 'length')),
			('winner', self.winner, True),
			('vod', self.getValue('vodgame' + str(self.index)), True),
			('vod', self.getValue('vod' + str(self.index)), True)
		])

		return self.generateString(out)
