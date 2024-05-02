r"""
This bot will make direct text replacements.

It will retrieve old match groups and convert them into Match2 groups

These command line parameters can be used to specify which templates to convert

&params;

Furthermore, the following command line parameters are supported:

-singlematch Used to convert old Showmatch into SingleMatch

-matchlist Used to convert MatchList into Matchlist

-matchliststart Used to convert MatchListStart etc. to Matchlist

-bracket Used to convert XBracket to Bracket|

-oldTemplateId Name of the template that is currently being used on the page

IF -matchliststart you need to specify the match templates with -matchTemplateId
 ("MatchMaps") and the end template with -endTemplateId ("MatchListEnd")

If -bracket and template is not Legacy you need to specify the new bracket id
 with -newBracketId (something like "Bracket/2") and bracket type with
 -bracketType ("team", "solo", ...)

Examples
--------

python pwb.py convert_matchgroup -lang:valorant -page:"User:LuckeLucky/sandbox/2" -bracket -oldTemplateId:"LegacyBracket"
python pwb.py convert_matchgroup -lang:fifa -matchlist -page:"EK League/2022/Preseason/Club" -bracketType:"team" -oldTemplateId:"MatchList"

"""
import sys
from typing import List

import mwparserfromhell

import pywikibot
from pywikibot import pagegenerators
from scripts.match2.commons.template import Template
from scripts.match2.commons.utils import generateId, importClass
from scripts.utils import get_text, put_text, remove_and_squash


BRACKET = 'Bracket'
MATCHLIST = 'Matchlist'
MATCHGROUPS = ['singlematch', 'matchlist', 'bracket']

class MatchGroupConverter:
	def __init__(self) -> None:
		self.language: str = ''
		self.newTemplateId: str = ''
		self.isLegacy: bool = False
		self.isMatchListStart: bool = False

		#used for bracket
		self.oldTemplateId: str = ''
		self.newBracketId: str = ''
		self.bracketType: str = ''

		#used for matchliststart
		self.matchTemplateId: str = ''
		self.endTemplateId: str = ''

		self.matchGroupClass = None

	def handleDefaultArg(self, arg: str) -> bool:
		arg = arg[1:]
		arg, _, value = arg.partition(':')
		if hasattr(self, arg):
			setattr(self, arg, value)
			return True
		if arg in MATCHGROUPS:
			self.newTemplateId = arg.capitalize()
			return True
		return False

	def getSummary(self) -> str:
		return f'Convert {self.oldTemplateId} to Match2'

	def check(self):
		if not self.oldTemplateId:
			self.oldTemplateId = pywikibot.input('Old template id:')

		if self.oldTemplateId.startswith('Legacy'):
			self.isLegacy = True

		if not self.bracketType and self.oldTemplateId != 'LegacyBracket':
			self.bracketType = self.bracketType or pywikibot.input('Bracket type:')

		self.matchGroupClass = importClass(self.language, self.newTemplateId)

		if self.newTemplateId == BRACKET and not self.isLegacy:
			self.newBracketId = self.newBracketId or pywikibot.input('New bracket id:')

		if self.isMatchListStart:
			self.matchTemplateId = self.matchTemplateId or pywikibot.input('Match template id:')
			self.endTemplateId = self.endTemplateId or pywikibot.input('End template id:')


	def addStuffToTemplate(self, template):
		if self.isLegacy:
			return template
		if self.newTemplateId == BRACKET:
			template.addIfNotHas('1', self.newBracketId)
			template.addIfNotHas('2', self.oldTemplateId)
		template.addIfNotHas('type', self.bracketType)
		template.addIfNotHas('id', generateId())
		return template

	def convertBracket(self, text: str) -> str:
		wikicode = mwparserfromhell.parse(text)
		for template in wikicode.filter_templates():
			if template.name.matches(self.oldTemplateId):
				t = self.addStuffToTemplate(Template(template, removeComments=True))
				newBracket = self.matchGroupClass(t)
				if not newBracket.bDM.isTemplateSupported(newBracket.newTemplateId):
					pywikibot.stdout("<<lightred>>Missing support for template " + newBracket.newTemplateId)
					sys.exit(1)
				wikicode.replace(template, str(newBracket))

		return str(wikicode)

	def convertSinglematch(self, text: str) -> str:
		wikicode = mwparserfromhell.parse(text)
		for template in wikicode.filter_templates():
			if template.name.matches(self.oldTemplateId):
				t = self.addStuffToTemplate(Template(template, removeComments=True))
				newSingleMatch = self.matchGroupClass(t)
				wikicode.replace(template, str(newSingleMatch))

		return str(wikicode)

	def _convertMatchlist(self, text: str) -> str:
		wikicode = mwparserfromhell.parse(text)
		for template in wikicode.filter_templates():
			if template.name.matches(self.oldTemplateId):
				t: Template = self.addStuffToTemplate(Template(template))
				matches: List[Template] = []
				for key, _ in t.iterateByPrefix('match'):
					matches.append(Template(t.getNestedTemplate(key)))
				newMatchList = self.matchGroupClass(t, matches)
				wikicode.replace(template, str(newMatchList))
		return str(wikicode)

	def _convertMatchliststart(self, text: str) -> str:
		while True:
			matchListStart: Template = None
			matches: List[Template] = []
			templatesToRemove: List[Template] = []
			start = False
			ends = False

			wikicode = mwparserfromhell.parse(text)
			for template in wikicode.filter_templates():
				if template.name.matches(self.oldTemplateId):
					start = True
					matchListStart = template
					matches = []
					templatesToRemove = []
				elif start and template.name.matches(self.matchTemplateId):
					matches.append(Template(template))
					templatesToRemove.append(template)
				elif start and template.name.matches(self.endTemplateId):
					templatesToRemove.append(template)
					start = False
					ends = True
					break

			if not ends or len(matches) == 0:
				break

			t: Template = self.addStuffToTemplate(Template(matchListStart))

			newMatchList = self.matchGroupClass(t, matches)
			wikicode.replace(matchListStart, str(newMatchList))
			for template in templatesToRemove:
				remove_and_squash(wikicode, template)

			text = str(wikicode)
		return str(wikicode)

	def convertMatchlist(self, text: str) -> str:
		if self.isMatchListStart:
			return self._convertMatchliststart(text)
		return self._convertMatchlist(text)

	def convert(self, text: str) -> str:
		converter = getattr(self, 'convert' + self.newTemplateId)
		if not converter:
			raise ValueError(self.newTemplateId + 'is not supported')
		return converter(text)

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
				converter.newTemplateId = MATCHLIST
				converter.isMatchListStart = True

	if not converter.newTemplateId:
		pywikibot.stdout("Match Group needs to be specified p.ex -singlematch")
		sys.exit(1)

	converter.language = genFactory.site.code

	converter.check()

	editSummary = converter.getSummary()

	generator = genFactory.getCombinedGenerator()
	for page in generator:
		text = get_text(page)
		newText = converter.convert(text)
		if text != newText:
			if save:
				put_text(page, newText, editSummary)
			else:
				print(newText)

if __name__ == '__main__':
	main()
