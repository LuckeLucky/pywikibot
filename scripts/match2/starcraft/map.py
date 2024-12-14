from typing import List
from ..commons.map import Map as commonsMap

MAX_NUMBER_OF_OPPONENTS = 2

class Map(commonsMap):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Map', indent = '', end = '}}')

	def getDefaultOut(self, mapName: str, winner: str) -> List:
		hasScores = self.template.getfirstValueFound([self.prefix + 'p1score', self.prefix + 'p2score'])
		walkover = self.getValue(self.prefix + 'walkover')

		if not mapName and hasScores:
			mapName = f'Submatch {self.index}'

		out = [
			('map', mapName),
			('winner', winner, winner and not walkover),
			('walkover', walkover, walkover == '')
		]

		if hasScores:
			out.extend([
				('score1', self.getValue(self.prefix + 'p1score')),
				('score2', self.getValue(self.prefix + 'p2score')),
			])
		out.append(('subgroup', self.getValue('subgroup'), True))

		return out

	def getTeamPlayersOut(self, teamIndex: int, playerIndex: int, m1key: str) -> List:
		m2key = f't{teamIndex}p{playerIndex}'
		link = self.getValue(m1key + 'link') if self.getValue(m1key + 'link') and self.getValue(m1key + 'link') != 'false' else ''
		return [
			(f'{m2key}', self.getValue(m1key), True),
			(f'{m2key}link', link, True),
			(f'{m2key}flag', self.getValue(m1key + 'flag'), True),
			(f'{m2key}race', self.getValue(m1key + 'race'), True),
		]

	def getPlayersOut(self, isDuo: bool, match1KeyMaker) -> List:
		out = []
		playerIndex = 1
		isLegacy = str(self.template._name).endswith('Legacy2v2')

		for oppIndex in range(1, MAX_NUMBER_OF_OPPONENTS +1):
			out.extend(self.getTeamPlayersOut(oppIndex, 1, match1KeyMaker(oppIndex if isLegacy else playerIndex)))
			playerIndex += 1
			if isDuo:
				out.extend(self.getTeamPlayersOut(oppIndex, 2, match1KeyMaker(oppIndex + 2 if isLegacy else playerIndex)))
				playerIndex += 1
			elif self.getValue('2v2') == str(self.index):
				out.extend(self.getTeamPlayersOut(oppIndex, 2, f'2v2p{oppIndex}'))

		return out

	def normalStr(self) -> str:
		out = self.getDefaultOut(self.getValue(self.prefix), self.getValue(self.prefix + 'win'))
		isDuo = self.getValue(self.prefix + 'p3') != ''
		out.extend(self.getPlayersOut(isDuo, lambda pIndex: f'{self.prefix}p{pIndex}'))
		out.append(('vod', self.template.getfirstValueFound([self.prefix + 'vod', f'vod{self.index}']), True))

		return self.generateString([out])

	def __str__(self) -> str:
		if not str(self.template._name).startswith('MatchMaps/Legacy'):
			return self.normalStr()

		out = []
		if self.getValue('subgroup'):
			out = self.getDefaultOut(self.getValue('map1'), self.getValue('map1win'))
		else:
			out = self.getDefaultOut(self.getValue('map1'), self.getValue('winner'))
		isDuo = str(self.template._name).endswith('2v2')
		out.extend(self.getPlayersOut(isDuo, lambda pIndex: f'player{pIndex}'))
		out.append(('vod', self.template.getfirstValueFound(['vod', 'vodgame1']), True))

		return self.generateString([out])