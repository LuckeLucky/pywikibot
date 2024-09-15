import re

from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def subMap(self, out: str) -> str:
		return (
			out +
			f'{self.indent}|t1p1={self.getValue(self.prefix + 't1p1')} ' +
			f'|t1p1flag={self.getValue(self.prefix + 't1p1flag')} ' +
			f'|t2p1={self.getValue(self.prefix + 't2p2')} ' +
			f'|t2p1flag={self.getValue(self.prefix + 't2p2flag')}\n'
		)

	def fixScore(self):
		for i in range(0, 2):
			index = i+1
			score = self.getValue(self.prefix + 't' + str(index) + 'score')
			if '(' in score:
				match = re.match(r'(\d*)\s*\((\d*)\)', score)
				if match:
					self.template.add(self.prefix + 't' + str(index) + 'score', match.groups()[0])
					self.template.add(self.prefix + 't' + str(index) + 'pscore', match.groups()[1])


	def __str__(self) -> str:
		indent = self.indent
		self.fixScore()
		out = (
			'{{Map' + 
			f'|winner={self.getValue(self.prefix + 'win')}\n' +
		 	f'{indent}|score1={self.getValue(self.prefix + 't1score')} ' +
			f'|score2={self.getValue(self.prefix + 't2score')}\n'
		)

		if (self.getValue(self.prefix + 't1pscore') or
			self.getValue(self.prefix + 't2pscore')):
			out = (
				out +
				f'{self.indent}|penaltyScore1={self.getValue(self.prefix + 't1pscore')} ' +
				f'|penaltyScore2={self.getValue(self.prefix + 't2pscore')}\n'
			)

		if self.getValue('hasSubmatches'):
			out = self.subMap(out)

		vod = self.getValue('vodgame' + str(self.index))
		if vod:
			out += f'{indent}|vod={vod}\n'

		mapName = self.template.getfirstValueFound([self.prefix, self.prefix + 'stadium'])
		if mapName:
			out += f'{indent}|map={mapName}\n'

		out += indent[:len(indent)//2] + "}}"
		return out
