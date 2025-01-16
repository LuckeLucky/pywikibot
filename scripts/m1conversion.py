r"""

"""

from typing import List

import mwparserfromhell

import pywikibot
from pywikibot import pagegenerators
from scripts.match2.commons.template import Template
from scripts.utils import get_text, put_text, remove_and_squash

BRACKET = 'bracket'
MATCHLIST = 'matchlist'
MATCHGROUPS = [BRACKET, MATCHLIST, 'singlematch']
REQUIRED_ARGS = ['oldTemplateId', 'matchGroupType', 'opponentType']

class MatchGroupConverter:
	def __init__(self) -> None:
		self.newTemplateId: str = None
		self.isMatchListStart: bool = False

		#used for all
		self.oldTemplateId: str = None
		self.matchGroupType: str = None
		self.opponentType: str = None

		#used for bracket
		self.newBracketId: str = None

		#used for matchliststart
		self.matchTemplateId: str = None
		self.endTemplateId: str = None

	def handleDefaultArg(self, arg: str) -> bool:
		arg = arg[1:]
		arg, _, value = arg.partition(':')
		if hasattr(self, arg):
			setattr(self, arg, value)
			return True
		return False

	def getSummary(self) -> str:
		return f'Convert {self.oldTemplateId} to Match2'

	def check(self) -> None:
		newTemplateId = 'subst:#invoke:M1Conversion/Custom|run'
		for rarg in REQUIRED_ARGS:
			if getattr(self, rarg) is None:
				value = pywikibot.input(f'Argument {rarg} is required, input value:')
				setattr(self, rarg, value)
			newTemplateId += f'|{rarg}={getattr(self, rarg)}'

		if self.matchGroupType == BRACKET:
			self.newBracketId = pywikibot.input('Argument newBracketId is required, input value:')\
				if self.newBracketId is None else self.newBracketId
			newTemplateId += f'|newBracketId={self.newBracketId}'
		elif self.isMatchListStart and (self.matchTemplateId is None or\
				self.endTemplateId is None):
			self.matchTemplateId = pywikibot.input('Argument matchTemplateId is required, input value:')\
				if self.matchTemplateId is None else self.matchTemplateId
			self.endTemplateId = pywikibot.input('Argument endTemplateId is required, input value:')\
				if self.endTemplateId is None else self.endTemplateId

		self.newTemplateId = newTemplateId

	def invokeJson(self, template: mwparserfromhell.nodes.Template) -> str:
		template.name = self.newTemplateId
		cleaned = Template.initFromTemplate(template)
		return str(cleaned).replace('={{', '={{subst:#invoke:Json|fromArgs|templateName=')

	def _matchliststartConvert(self, text: str) -> str:
		while True:
			matchListStart: Template = None
			matches: List[Template] = []
			templatesToRemove: List[Template] = []
			start = False
			ends = False

			wikicode = mwparserfromhell.parse(text)
			for template in wikicode.filter_templates(recursive = False):
				if template.name.matches(self.oldTemplateId):
					start = True
					matchListStart = template
					matches = []
					templatesToRemove = []
				elif start and template.name.matches(self.matchTemplateId):
					matchListStart.add('match' + str(len(matches)+1), str(template))
					matches.append(template)
					templatesToRemove.append(template)
				elif start and template.name.matches(self.endTemplateId):
					templatesToRemove.append(template)
					start = False
					ends = True
					break

			if not ends or len(matches) == 0:
				break

			wikicode.replace(matchListStart, self.invokeJson(matchListStart))
			for template in templatesToRemove:
				remove_and_squash(wikicode, template)

			text = str(wikicode)
		return str(wikicode)

	def _defaultConvert(self, text: str) -> str:
		wikicode = mwparserfromhell.parse(text)
		for t in wikicode.filter_templates(matches = lambda t: t.name.matches(self.oldTemplateId)):
			wikicode.replace(t, self.invokeJson(t))

		return str(wikicode)

	def getConverter(self):
		if self.isMatchListStart:
			return self._matchliststartConvert
		return self._defaultConvert

def main(*args):
	# Read commandline parameters.
	localArgs = pywikibot.handle_args(args)
	genFactory = pagegenerators.GeneratorFactory()
	converter = MatchGroupConverter()

	save = True
	for arg in localArgs:
		if genFactory.handle_arg(arg):
			continue
		if converter.handleDefaultArg(arg):
			continue
		if arg.startswith('-'):
			arg, _, _ = arg.partition(':')
			if arg == '-nosave':
				save = False
			if arg == '-matchliststart':
				converter.matchGroupType = MATCHLIST
				converter.isMatchListStart = True

	converter.check()
	editSummary = converter.getSummary()
	converterFn = converter.getConverter()

	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = converterFn(text)
		if text != newText:
			if save:
				put_text(page, newText, editSummary)
			else:
				print(newText)

if __name__ == '__main__':
	main()
