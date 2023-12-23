import mwparserfromhell

from scripts.match2.commons.template import Template
from scripts.match2.counterstrike.bracket import BracketCounterstrike
from tests.aspects import TestCase

class TestBracketLeague(TestCase):
	net = False
	maxDiff = None

	def testCounterstrikeConvert(self):
		text = ("{{2SETeamBracket\n" +
			"|R1D1team=saw |R1D1score=1 |R1D1win=\n" +
			"|R1D2team=ftw |R1D2score=2 |R1D2win=1\n" +
			"|R1G1details={{BracketMatchSummary\n" +
			"|date=December 20, 2023 - 11:00 {{Abbr/CEST}} |finished=true\n" +
			"|twitch=\n" +
			"|map1t1firstside=ct|map1t1t=11|map1t1ct=5|map1t2t=10|map1t2ct=0\n" +
			"|map1=Overpass|map1score=|map1win=1|vodgame1=|stats1=168110\n" +
			"|map2t1firstside=t|map2t1t=2|map2t1ct=0|map2t2t=3|map2t2ct=13\n" +
			"|map2=Ancient|map2score=|map2win=2|vodgame2=|stats2=168105\n" +
			"|map3t1firstside=t|map3t1t=14|map3t1ct=0|map3t2t=15|map3t2ct=1\n" +
			"|map3=Vertigo|map3score=|map3win=2|vodgame3=|stats3=168136\n" +
			"|hltv=2368518}}}}\n"
		)
		oldTemplate = mwparserfromhell.parse(text).filter_templates()[0]

		bracket = BracketCounterstrike(Template(oldTemplate))
		bracket.oldTemplateId = '2SETeamBracket'
		bracket.newTemplateId = 'Bracket/2'
		bracket.id = 'TESTID'
		bracket.bracketType = 'team'
		bracket.process()

		expected = ("{{Bracket|Bracket/2|id=TESTID\n" +
            "\n" +
            "<!-- Grand Final -->\n" +
            "|R1M1={{Match\n" +
            "\t|opponent1={{TeamOpponent|saw|score=1}}\n" +
            "\t|opponent2={{TeamOpponent|ftw|score=2}}\n" +
            "\t|date=December 20, 2023 - 11:00 {{Abbr/CEST}} |finished=true\n" +
            "\t|winner=2\n" +
            "\t|twitch=\n" +
            "\t|hltv=2368518\n" +
            "\t|map1={{Map|map=Overpass|finished=true\n" +
            "\t\t|t1firstside=ct|t1t=11|t1ct=5|t2t=10|t2ct=0\n" +
            "\t\t|stats=168110\n" +
            "\t}}\n" +
            "\t|map2={{Map|map=Ancient|finished=true\n" +
            "\t\t|t1firstside=t|t1t=2|t1ct=0|t2t=3|t2ct=13\n" +
            "\t\t|stats=168105\n" +
            "\t}}\n" +
            "\t|map3={{Map|map=Vertigo|finished=true\n" +
            "\t\t|t1firstside=t|t1t=14|t1ct=0|t2t=15|t2ct=1\n" +
            "\t\t|stats=168136\n" +
            "\t}}\n" +
            "}}\n}}"
		)
		self.assertEqual(expected, str(bracket))
