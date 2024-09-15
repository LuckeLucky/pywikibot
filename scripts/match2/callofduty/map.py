from ..commons.map import Map as commonsMap

SKIP = 'skip'

class Map(commonsMap):
	def __str__(self) -> str:
		playedMap = self.getValue(self.prefix)
		winner = self.getValue(self.prefix + 'win')
		if not winner and playedMap:
			winner = SKIP
		out = (
			'{{Map' +
			f'|map={playedMap}' +
			self.printParam(self.prefix + 'type', 'mode', True)
		)

		score = self.getValue(self.prefix + 'score')
		if score and '-' in score:
			splitScore = score.split('-', 1)
			out = (
				out +
				f'|score1={splitScore[0]}'
				f'|score2={splitScore[1]}'
			)

		out = (
			out +
			f'|winner={winner}' +
			self.printParam('vodgame' + str(self.index), 'vod', True)
		)

		return out + '}}'
