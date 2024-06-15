from ..commons.map import Map as commonsMap

class Map(commonsMap):
	def getPrefixedParams(self, prefix: str) -> str:
		result = ""
		for key, value in self.template.iterateByPrefix(prefix):
			result += f"|{key}={value}"
		return result

	def __str__(self) -> str:
		out = []
		score = self.getValue(self.prefix + 'score')
		if score and '-' in score:
			splitScore = score.split('-', 1)
			out.append(' '.join([
				f'|score1={splitScore[0]}',
				f'|score2={splitScore[1]}',
				self.printParam(self.prefix + 'win', 'winner', ignoreIfEmpty=True, end='\n'),
			]))
		else:
			out.append(self.printParam(self.prefix + 'win', 'winner', ignoreIfEmpty=True, end='\n'))
		out.append(self.printParam(f'vodgame{self.index}', 'vod', ignoreIfEmpty=True, end='\n'))

		return self.print(out)
