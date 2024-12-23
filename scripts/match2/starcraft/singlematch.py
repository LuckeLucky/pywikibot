from scripts.match2.commons.opponent import Opponent, SoloOpponent
from ..commons.template import Template
from ..commons.singlematch import Singlematch as CommonsSinglematch

MAX_NUMBER_OPPONENTS = 2

class Singlematch(CommonsSinglematch):
	def getSoloOpponent(self, key: str, scoreKey: str) -> Opponent:
		keyMaker = lambda key, prefix : key + prefix
		if self.template._name == 'MatchSummary':
			keyMaker = lambda key, prefix: prefix + key

		name = self.getValue(keyMaker(key, ''))
		link = self.getValue(keyMaker(key, 'link'))
		flag = self.getValue(keyMaker(key, 'flag'))
		race = self.getValue(keyMaker(key, 'race'))
		score = self.getValue(scoreKey)

		if link == 'false':
			link = ''

		return SoloOpponent(name = name, link = link, flag = flag, race = race, score = score)

	def getMatch(self):
		opponentKey = ''
		scoreKey = ''
		details = None
		if self.template._name in ['FTeamMatch', 'Proleague06Match', 'Proleague04-05Match',
							'TeamMatch', 'TeamMatchBo3', 'TeamMatchWith2v2', 'ProleagueMatchBo9', 'ProleagueMatch',
							'TeamMatchListHeader', 'ProleagueMatchNL']:
			opponentKey = 'team$'
			details = self.template
			if self.template._name in ['TeamMatch', 'TeamMatchBo3', 'TeamMatchWith2v2', 'TeamMatchListHeader']:
				self.template.add('team1', self.template.getfirstValueFound(['team1', 'team1short', 'team1literal']))
				self.template.add('team2', self.template.getfirstValueFound(['team2', 'team2short', 'team2literal']))
				self.template.add('winner', self.getValue('teamwin'))
			if self.template._name == 'TeamMatchListHeader':
				scoreKey = 'team$score'
		elif self.template._name == 'MatchSummary':
			opponentKey = '$'
			details = self.template
		elif self.template._name == 'Showmatch':
			opponentKey = 'p$'
			scoreKey = 'score'
			winner = self.getValue('win')
			details = self.template.getNestedTemplate('details')
			if winner:
				if not details:
					details = Template.createFakeTemplate()
				details.add('winner', winner)
			details = Template(details)
		elif self.template._name == 'TeamMatchListHeader':
			opponentKey = 'team$'
			scoreKey = 'team$score'
			winner = self.getValue('teamwin')
			if winner:
				self.template.add('winner', winner)
			details = self.template

		if opponentKey or scoreKey:
			opponents = []
			for i in range(1, MAX_NUMBER_OPPONENTS+1):
				strIndex = str(i)
				opponents.append(self.getOpponent(
					self.template,
					opponentKey.replace('$', strIndex),
					scoreKey.replace('$', strIndex)
				))
			self.match = self.matchClass(opponents, details)
		else:
			super().getMatch()
