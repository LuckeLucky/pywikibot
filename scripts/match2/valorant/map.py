from ..commons.template import Template

from ..commons.map import Map as commonsMap

MAX_NUMBER_OF_OPPONENTS = 2
MAX_NUMBER_OF_PLAYERS = 5

SKIP = 'skip'

class Map(commonsMap):
	def __init__(self, index: int, template: Template) -> None:
		super().__init__(index, template)
		winner = self.template.getValue(self.prefix + 'win')
		if winner in ['1', '2', '0']:
			self.winner = int(winner)
			self.finished = 'true'
		elif winner == 'draw':
			self.winner = 0
			self.finished = 'true'
		elif winner == SKIP:
			self.winner = ''
			self.finished = SKIP
		else:
			self.winner = ''
			self.finished = ''
		score = self.template.getValue(self.prefix + 'score')
		self.score = score.split('-', 1)

	def getPlayerStats(self, oppIndex: int, playerIndex: int) -> (str, bool):
		teamX = self.prefix + 't' + str(oppIndex)
		pIdx = str(playerIndex)
		player = self.template.getValue(teamX + 'p' + pIdx)
		agent = self.template.getValue(teamX + 'a' + pIdx)
		acs = self.template.getValue(teamX + 'acs' + pIdx)
		kda = self.template.getValue(teamX + 'kda' + pIdx)
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
		indent = "  "

		if self.finished == SKIP:
			return f"{{{{Map|map={self.template.getValue(self.prefix)} |finished={self.finished}}}}}\n"

		out = "{{Map\n"
		for oppIndex in range(1, MAX_NUMBER_OF_OPPONENTS+1):
			teamStatsOut = []
			hasTeamStats = False
			for playerIndex in range(1, MAX_NUMBER_OF_PLAYERS+1):
				playerOut, ok = self.getPlayerStats(oppIndex, playerIndex)
				if ok:
					hasTeamStats = True
				teamStatsOut.append(f'|t{oppIndex}p{playerIndex}={playerOut}')
			if hasTeamStats:
				teamOut = '\n'.join(indent + so for so in teamStatsOut)
				out += teamOut + '\n\n'

		hasHalfScores = False
		if self.template.getValue(self.prefix + 't1firstside'):
			hasHalfScores = True
			out += (
				indent +
				f'|t1firstside={self.template.getValue(self.prefix + 't1firstside')}' +
				f'|t1atk={self.template.getValue(self.prefix + 't1atk')}' +
				f'|t1def={self.template.getValue(self.prefix + 't1def')}' +
				f'|t2atk={self.template.getValue(self.prefix + 't2atk')}' +
				f'|t2def={self.template.getValue(self.prefix + 't2def')}\n'
			)

		if self.template.getValue(self.prefix + 'o1t1firstside'):
			out += (
				indent +
				f'|t1firstsideot={self.template.getValue(self.prefix + 'o1t1firstside')}' +
				f'|t1otatk={self.template.getValue(self.prefix + 'o1t1atk')}' +
				f'|t1otdef={self.template.getValue(self.prefix + 'o1t1def')}' +
				f'|t2otatk={self.template.getValue(self.prefix + 'o1t2atk')}' +
				f'|t2otdef={self.template.getValue(self.prefix + 'o1t2def')}\n'
			)

		if not hasHalfScores:
			out += indent + f"|score1={self.score[0]}|score2={self.score[1]}\n"

		vod = self.template.getValue('vod' + str(self.index))
		if not vod:
			vod = self.template.getValue('vodgame' + str(self.index))
		out += (
			indent +
			f'|map={self.template.getValue(self.prefix)}' +
			f'|finished={self.finished}' +
			f'|length={self.template.getValue(self.prefix + 'length')}'
		)

		if self.winner:
			out += f'|winner={self.winner}'

		if vod:
			out += f'|vod={vod}'

		out += '\n'
		out += indent + '}}'
		return out
