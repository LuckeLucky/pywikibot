from typing import List

from ..commons.map import Map as commonsMap

MAPTOMODE = {
	'control' : 'Control',
	'busan' : 'Control',
	'ilios' : 'Control',
	'lijiang tower' : 'Control',
	'nepal' : 'Control',
	'oasis' : 'Control',
	'escort' : 'Escort',
	'circuit royal' : 'Escort',
	'dorado' : 'Escort',
	'havana' : 'Escort',
	'junkertown' : 'Escort',
	'shambali monastery' : 'Escort',
	'rialto' : 'Escort',
	'route 66' : 'Escort',
	'gibraltar' : 'Escort',
	'watchpoint: gibraltar' : 'Escort',
	'hybrid' : 'Hybrid',
	'blizzard world' : 'Hybrid',
	'eichenwalde' : 'Hybrid',
	'hollywood' : 'Hybrid',
	'king\'s row' : 'Hybrid',
	'midtown' : 'Hybrid',
	'numbani' : 'Hybrid',
	'paraiso' : 'Hybrid',
	'paraíso' : 'Hybrid',
	'push' : 'Push',
	'colosseo' : 'Push',
	'esperanca' : 'Push',
	'esperança' : 'Push',
	'new queen street' : 'Push',
	'ayutthaya' : 'Assault',
	'black forest' : 'Assault',
	'castillo' : 'Assault',
	'château guillard' : 'Assault',
	'ecopoint: antarctica' : 'Assault',
	'kanezaka' : 'Assault',
	'malevento' : 'Assault',
	'necropolis' : 'Assault',
	'petra : Arena' : 'Assault',
	'assault' : 'Assault',
	'hanamura' : 'Assault',
	'horizon lunar colony' : 'Assault',
	'paris' : 'Assault',
	'temple of anubis' : 'Assault',
	'volskaya' : 'Assault',
	'volskaya industries' : 'Assault',
}

class Map(commonsMap):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Map', indent = '', end = '}}')

	def getMode(self, mapName: str) -> str:
		return MAPTOMODE.get(mapName.lower(), '')

	def __str__(self) -> str:
		out = [
			('map', self.getValue('map')),
			('mode', self.getMode(self.getValue('map'))),
		]

		score = self.getValue('score')
		if score and '-' in score:
			splitScore = score.split('-', 1)
			out.extend([
				('score1', splitScore[0]),
				('score2', splitScore[1]),
			])
		out.append(('vod', self.getValue('vod'), True))
		out.append(('winner', self.getValue('win')))

		return self.generateString([out])
