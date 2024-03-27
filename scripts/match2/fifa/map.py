from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def subMap(self, out: str) -> str:
		out = (
			out +
			f'{self.indent}|penaltyScore1={self.template.getValue(self.prefix + 't1pscore')} ' +
			f'|penaltyScore2={self.template.getValue(self.prefix + 't2pscore')}\n'
			f'{self.indent}|t1p1={self.template.getValue(self.prefix + 't1p1')} ' +
			f'|t1p1flag={self.template.getValue(self.prefix + 't1p1flag')} ' +
			f'|t2p1={self.template.getValue(self.prefix + 't2p2')} ' +
			f'|t2p1flag={self.template.getValue(self.prefix + 't2p2flag')}\n'
		)

		return out

	def __str__(self) -> str:
		indent = self.indent
		out = (
			'{{Map' + 
			f'|winner={self.template.getValue(self.prefix + 'win')}\n' +
		 	f'{indent}|score1={self.template.getValue(self.prefix + 't1score')} ' +
			f'|score2={self.template.getValue(self.prefix + 't2score')}\n'
		)
		if self.template.getValue('hasSubmatches'):
			out = self.subMap(out)

		vod = self.template.getValue('vodgame' + str(self.index))
		if vod:
			out += f'{indent}|vod={vod}\n'

		mapName = self.template.getfirstValueFound([self.prefix, self.prefix + 'stadium'])
		if mapName:
			out += f'{indent}|map={mapName}\n'

		out += indent[:len(indent)//2] + "}}"
		return out
