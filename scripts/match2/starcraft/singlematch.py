from scripts.match2.commons.opponent import Opponent, SoloOpponent
from ..commons.template import Template
from ..commons.singlematch import Singlematch as CommonsSinglematch

class Singlematch(CommonsSinglematch):
	def getSoloOpponent(self, key: str, scoreKey: str) -> Opponent:
		name = self.template.getValue(key)
		link = self.template.getValue(key + 'link')
		flag = self.template.getValue(key + 'flag')
		race = self.template.getValue(key + 'race')
		score = self.template.getValue(scoreKey)

		if link == 'false':
			link = ''

		return SoloOpponent(name = name, link = link, flag = flag, race = race, score = score)

	def getMatch(self):
		if self.template.name in ['FTeamMatch', 'Proleague06Match', 'Proleague04-05Match']:
			opponent1 = self.getOpponent('team1', '')
			opponent2 = self.getOpponent('team2', '')
			self.match = self.matchClass([opponent1, opponent2], self.template)
		elif self.template.name == 'Showmatch':
			opponent1 = self.getSoloOpponent('p1', 'score1')
			opponent2 = self.getSoloOpponent('p2', 'score2')
			winner = self.template.getValue('win')
			details = self.template.getNestedTemplate('details')
			if winner:
				if not details:
					details = Template.createFakeTemplate()
				details.add('winner', winner)
			self.match = self.matchClass([opponent1, opponent2], Template(details))
		else:
			super().getMatch()
