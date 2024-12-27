from typing import List, Tuple
from copy import deepcopy

from scripts.match2.commons.opponent import Opponent
from ..commons.template import Template
from ..commons.match import Match as commonsMatch, STREAMS

from .map import Map

MAX_NUMBER_OF_MAPS = 10

class Match(commonsMatch):
	def _iterateMaps(self, totalMaps: int, scores: List[int], prefix: str, currentSubgroup: int) -> Tuple[int, List[int], int]:
		for mapIndex in range(1, MAX_NUMBER_OF_MAPS if prefix == 'm' else 2):
			mapField = prefix + str(mapIndex) if prefix == 'm' else prefix # mX or acep
			details = {
				'o1p1': self.getValue(mapField + 'p1'),
				'o2p1': self.getValue(mapField + 'p2'),
				'vod': self.getValue(f'vod{currentSubgroup + 1}')
			}
			submatchWinner = ''
			p1score = self.getValue(f"{mapField}p1score")
			p2score = self.getValue(f"{mapField}p2score")
			if p1score and p2score:
				winner = 1 if int(p1score) > int(p2score) else 2
				scores[winner - 1] += 1
				submatchWinner = str(winner)

			currentSubgroup = currentSubgroup + 1
			hasMatches = False
			hasHeader = False
			for nestedMapIndex in range(1, MAX_NUMBER_OF_MAPS):
				mapWinner = self.getValue(f'{mapField}win{nestedMapIndex}')
				#No map by map details
				if (nestedMapIndex == 1 and
					not mapWinner and
					p1score and
					p2score):

					details.update({
						'map': f'Submatch {currentSubgroup}',
						'score1': p1score,
						'score2': p2score,
						'winner': submatchWinner
					})
					totalMaps += 1
					newMap = Map(totalMaps, Template.initFromDict('fake', details))
					if not hasHeader and prefix == 'ace':
						newMap.header = 'Ace Match'
						hasHeader = True
					newMap.subgroup = currentSubgroup
					self.maps.append(newMap)
					hasMatches = True
					break
				
				if not mapWinner or mapWinner.lower() == 'skip':
					break

				nestedDetails = deepcopy(details)
				nestedDetails.update({
					'subgroup': str(currentSubgroup),
					'o1c1': self.getValue(f'{mapField}p1class{nestedMapIndex}'),
					'o2c1': self.getValue(f'{mapField}p2class{nestedMapIndex}'),
					'winner': mapWinner
				})
				totalMaps += 1
				newMap = Map(totalMaps, Template.initFromDict('fake', nestedDetails))
				if not hasHeader and prefix == 'ace':
					newMap.header = 'Ace Match'
					hasHeader = True
				newMap.subgroup = currentSubgroup
				self.maps.append(newMap)
				hasMatches = True

			if not hasMatches:
				currentSubgroup = currentSubgroup - 1

		return totalMaps, scores, currentSubgroup

	def populateMaps(self):
		scores = [0, 0]
		totalMaps = 0
		totalMaps, scores, currentSubgroup = self._iterateMaps(totalMaps, scores, 'm', 0)
		_ , scores, _ = self._iterateMaps(totalMaps, scores, 'ace', currentSubgroup)

		self.opponents[0].score = str(scores[0])
		self.opponents[0].kwargs['score'] = str(scores[0])
		self.opponents[1].score = str(scores[1])
		self.opponents[1].kwargs['score'] = str(scores[1])

	def __str__(self) -> str:
		out = [
			[('date', self.getValue('date')), ('finished', 'true' if self.getValue('winner') else '')],
			self.getFoundMatches(STREAMS),
			('vod', self.getValue('vod')),
			('opponent1', str(self.opponents[0])),
			('opponent2', str(self.opponents[1])),
			('comment', self.getValue('comment'), True)
		]

		for matchMap in self.maps:
			if matchMap.header:
				out.append((f'subgroup{matchMap.subgroup}header', matchMap.header, True))
			out.append(('map' + str(matchMap.index), str(matchMap)))

		return self.generateString(out)
