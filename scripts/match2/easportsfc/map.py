from typing import List
import re

from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def fixScore(self):
		for i in range(0, 2):
			index = i+1
			score = self.getValue(self.prefix + 't' + str(index) + 'score')
			if '(' in score:
				match = re.match(r'(\d*)\s*\((\d*)\)', score)
				if match:
					self.template.add(self.prefix + 't' + str(index) + 'score', match.groups()[0])
					self.template.add(self.prefix + 't' + str(index) + 'pscore', match.groups()[1])

	def subMap(self) -> List:
		return [
			('t1p1', self.getValue(self.prefix + 't1p1')),
			('t1p1flag', self.getValue(self.prefix + 't1p1flag')),
			('t2p1', self.getValue(self.prefix + 't2p2')),
			('t2p1flag', self.getValue(self.prefix + 't2p2flag')),
		]

	def __str__(self) -> str:
		self.fixScore()
		out = [
			('winner', self.getValue(self.prefix + 'win')),
			[
				('score1', self.getValue(self.prefix + 't1score')),
				('score2', self.getValue(self.prefix + 't2score'))
			]
		]

		if self.getValue(self.prefix + 't1pscore') or self.getValue(self.prefix + 't2pscore'):
			out.append([
				('penaltyScore1', self.getValue(self.prefix + 't1pscore')),
				('penaltyScore2', self.getValue(self.prefix + 't2pscore'))
			])

		if self.getValue('hasSubmatches'):
			out.append(self.subMap())

		out.append(('vod', self.getValue('vodgame' + str(self.index)), True))
		out.append(('map', self.template.getfirstValueFound([self.prefix, self.prefix + 'stadium']), True))

		return self.generateString(out)

