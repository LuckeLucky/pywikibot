from ..commons.map import Map as commonsMap

MAX_NUMBER_OF_OPPONENTS = 2

class Map(commonsMap):
	def getPlayersOut(self, teamIndex: int, playerIndex: int, newIndex: int) -> str:
		m1key = self.prefix + 'p' + str(playerIndex)
		m2key = f't{teamIndex}p{newIndex}'
		out = (
				(f'|{m2key}={self.template.getValue(m1key)}' if self.template.getValue(m1key) else '') +
				(f'|{m2key}link={self.template.getValue(m1key + 'link')}' if self.template.getValue(m1key + 'link') else '') +
				(f'|{m2key}flag={self.template.getValue(m1key + 'flag')}' if self.template.getValue(m1key + 'flag') else '') +
				(f'|{m2key}race={self.template.getValue(m1key + 'race')}' if self.template.getValue(m1key + 'race') else '')
		)

		return out

	def __str__(self) -> str:
		out = ('{{Map' +
			f'|map={self.template.getValue(self.prefix)}' +
			f'|winner={self.template.getValue(self.prefix + 'win')}'
		)

		duo = self.template.getValue(self.prefix + 'p3')
		playerIndex = 1
		for i in range(1, MAX_NUMBER_OF_OPPONENTS+1):
			out += self.getPlayersOut(i, playerIndex, 1)
			playerIndex += 1
			if duo:
				out += self.getPlayersOut(i, playerIndex, 2)
				playerIndex += 1

		vod = self.template.getValue(self.prefix + 'vod')
		if vod:
			out += f'|vod={vod}'

		out = out +'}}'

		return out