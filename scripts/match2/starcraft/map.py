from ..commons.map import Map as commonsMap

MAX_NUMBER_OF_OPPONENTS = 2

class Map(commonsMap):
	def getPlayersOut(self, teamIndex: int, playerIndex: int, m1key: str) -> str:
		m2key = f't{teamIndex}p{playerIndex}'
		out = (
				(f'|{m2key}={self.getValue(m1key)}' if self.getValue(m1key) else '') +
				(f'|{m2key}link={self.getValue(m1key + 'link')}' if (
					self.getValue(m1key + 'link') and self.getValue(m1key + 'link') != 'false') else '') +
				(f'|{m2key}flag={self.getValue(m1key + 'flag')}' if self.getValue(m1key + 'flag') else '') +
				(f'|{m2key}race={self.getValue(m1key + 'race')}' if self.getValue(m1key + 'race') else '')
		)

		return out

	def geStartStr(self, mapName: str, winner: str) -> str:
		hasScores = self.template.getfirstValueFound([self.prefix + 'p1score', self.prefix + 'p2score'])
		walkover = self.getValue(self.prefix + 'walkover')

		if not mapName and hasScores:
			mapName = f'Submatch {self.index}'

		out = '{{Map'
		out += f'|map={mapName}'

		if winner and not walkover:
			out += f'|winner={winner}'
		if walkover:
			out += f'|walkover={walkover}'

		if hasScores:
			out += (
				f'|score1={self.getValue(self.prefix + 'p1score')}' +
				f'|score2={self.getValue(self.prefix + 'p2score')}'
			)

		subgroup = self.getValue('subgroup')
		if subgroup:
			out += f'|subgroup={subgroup}'

		return out

	def getPlayersStr(self, isDuo: bool, match1KeyMaker) -> str:
		out = ''
		playerIndex = 1
		isLegacy = str(self.template.name).endswith('Legacy2v2')

		for oppIndex in range(1, MAX_NUMBER_OF_OPPONENTS +1):
			out += self.getPlayersOut(oppIndex, 1, match1KeyMaker(oppIndex if isLegacy else playerIndex))
			playerIndex += 1
			if isDuo:
				out += self.getPlayersOut(oppIndex, 2, match1KeyMaker(oppIndex + 2 if isLegacy else playerIndex))
				playerIndex += 1
			elif self.getValue('2v2') == str(self.index):
				out += self.getPlayersOut(oppIndex, 2, f'2v2p{oppIndex}')

		return out

	def normalStr(self) -> str:
		out = self.geStartStr(self.getValue(self.prefix), self.getValue(self.prefix + 'win'))
		isDuo = self.getValue(self.prefix + 'p3') != ''
		out += self.getPlayersStr(isDuo, lambda pIndex: f'{self.prefix}p{pIndex}')

		vod = self.template.getfirstValueFound([self.prefix + 'vod', f'vod{self.index}'])
		if vod:
			out += f'|vod={vod}'

		out = out +'}}'

		return out

	def __str__(self) -> str:
		if not str(self.template.name).startswith('MatchMaps/Legacy'):
			return self.normalStr()

		out = ''
		if self.getValue('subgroup'):
			out = self.geStartStr(self.getValue('map1'), self.getValue('map1win'))
		else:
			out = self.geStartStr(self.getValue('map1'), self.getValue('winner'))
		isDuo = str(self.template.name).endswith('2v2')
		out += self.getPlayersStr(isDuo, lambda pIndex: f'player{pIndex}')
		vod = self.template.getfirstValueFound(['vod', 'vodgame1'])
		if vod:
			out += f'|vod={vod}'

		out = out +'}}'

		return out
