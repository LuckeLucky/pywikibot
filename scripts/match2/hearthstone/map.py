from typing import List
from ..commons.map import Map as commonsMap

MAX_NUMBER_OF_OPPONENTS = 2

class Map(commonsMap):
	def generateString(self, params: List[str]) -> str:
		return super().generateTemplateString(params, templateId = 'Map', indent = '', end = '}}')
	
	def __init__(self, index, template):
		super().__init__(index, template)
		self.header = ''
		self.subgroup = None

	def __str__(self) -> str:
		out = [
			('subgroup', self.getValue('subgroup'), True),
			('map', self.getValue('map'), True),
			('o1p1', self.getValue('o1p1')),
			('o1c1', self.getValue('o1c1'), True),
			('o2p1', self.getValue('o2p1')),
			('o2c1', self.getValue('o2c1'), True),
			('score1', self.getValue('score1'), True),
			('score2', self.getValue('score2'), True),
			('winner', self.getValue('winner')),
			('vod', self.getValue('vod'), True)
		]

		return self.generateString([out])