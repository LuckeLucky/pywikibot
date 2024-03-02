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
	def getMode(self, mapName: str) -> str:
		return MAPTOMODE.get(mapName.lower(), '')

	def __str__(self) -> str:
		mapValue, winner = None, None
		if self.template.name.matches('Match/old'):
			mapValue = self.template.getValue('map')
			winner = self.template.getValue('win')
		else:
			mapValue = self.template.getValue(self.prefix)
			winner = self.template.getValue(self.prefix + 'win')

		out = ("{{Map" +
		 	f'|map={mapValue}'
			f'|mode={self.getMode(mapValue)}'
		)

		score = self.template.getValue(self.prefix + 'score')
		if score and '-' in score:
			splitScore = score.split('-', 1)
			out += f'|score1={splitScore[0]}|score2={splitScore[1]}'

		vod = self.template.getValue('vodgame' + str(self.index))
		if vod:
			out += f'|vod={vod}'

		out += f'|winner={winner}'
		out += '}}'

		return out
