from scripts.match2.commons.opponent import Opponent, SoloOpponent
from ..commons.template import Template
from ..commons.singlematch import Singlematch as CommonsSinglematch

MAX_NUMBER_OPPONENTS = 2

class Singlematch(CommonsSinglematch):
	def getMatch(self):
		self.template.add('team1', self.template.getfirstValueFound(['team1', 'team1short', 'team1literal']))
		self.template.add('team2', self.template.getfirstValueFound(['team2', 'team2short', 'team2literal']))
		opponent1 = self.getOpponent('team1', 'team1score')
		opponent2 = self.getOpponent('team2', 'team2score')
		self.template.add('winner', self.getValue('teamwin'))
		self.match = self.matchClass([opponent1, opponent2], self.template)