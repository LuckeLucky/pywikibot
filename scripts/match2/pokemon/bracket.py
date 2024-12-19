from scripts.match2.commons.opponent import Opponent
from scripts.match2.commons.template import Template
from ..commons.bracket import Bracket as commonsBracket

class Bracket(commonsBracket):
	def __init__(self, template: Template) -> None:
		super().__init__(template)
		self.isMappingFixed = False
	def getWinner(self, team1Key: str, team2Key) -> str:
		if str(self.bracketType).lower() == 'solo' and team1Key[0] in ['r', 'l']:
			key = team1Key[:-2] + 'win'
			return self.getValue(key)
		return super().getWinner(team1Key, team2Key)

	def getSoloOpponent(self, template: Template, key: str, scoreKey: str) -> Opponent:
		val = template.get(key)
		val = val.replace('[[', '').replace(']]', '')
		val = val.replace("'", '')
		self.template.add(key, val)
		return super().getSoloOpponent(template, key, scoreKey)

	def fixDefaultMapping(self):
		currentMapping = self.bDM.defaultMapping[self.newTemplateId]
		for roundParam, match1Params in currentMapping.items():
			newKey = roundParam.lower()
			match1Params['details'] = newKey
			match1Params['opp1'] = newKey + 'p1'
			match1Params['opp2'] = newKey + 'p2'

		self.isMappingFixed = True

	def populateData(self):
		if (self.getValue('r1m1p1') or self.getValue('l1m1p1')) and not self.isMappingFixed:
			self.fixDefaultMapping()
		self._populateData(self.bDM.defaultMapping[self.newTemplateId])
		if self.mappingKey in self.bDM.customMapping:
			self._populateData(self.bDM.customMapping[self.mappingKey])
