import mwparserfromhell

from scripts.match2.commons.template import Template
from scripts.match2.counterstrike.bracket import Bracket as BracketCounterstrike
from scripts.match2.valorant.bracket import Bracket as BracketValorant
from scripts.match2.counterstrike.match import Match
from scripts.match2.commons.opponent import TeamOpponent
from tests.aspects import TestCase

RESET_MATCH = 'RxMBR'
THIRD_PLACE_MATCH = 'RxMTP'

class TestBracketLeague(TestCase):
	net = False
	maxDiff = None

	def testCounterstrikeConvert(self):
		text = """
		{{2SETeamBracket|R1=Ola
		|R1D1team=saw |R1D1score=1 |R1D1win=
		|R1D2team=ftw |R1D2score=2 |R1D2win=1
		|R1G1details={{BracketMatchSummary
		|date=December 20, 2023 - 11:00 {{Abbr/CEST}} |finished=true
		|twitch=
		|map1t1firstside=ct|map1t1t=11|map1t1ct=5|map1t2t=10|map1t2ct=0
		|map1=Overpass|map1score=|map1win=1|vodgame1=|stats1=168110
		|map2t1firstside=t|map2t1t=2|map2t1ct=0|map2t2t=3|map2t2ct=13
		|map2=Ancient|map2score=|map2win=2|vodgame2=|stats2=168105
		|map3t1firstside=t|map3t1t=14|map3t1ct=0|map3t2t=15|map3t2ct=1
		|map3=Vertigo|map3score=|map3win=2|vodgame3=|stats3=168136
		|hltv=2368518}}}}
		"""
		oldTemplate = mwparserfromhell.parse(text).filter_templates()[0]
		oldTemplate = Template(oldTemplate)
		oldTemplate.add('1', 'Bracket/2')
		oldTemplate.add('2', '2SETeamBracket')
		oldTemplate.add('id', 'TESTID')
		oldTemplate.add('type', 'team')

		bracket = BracketCounterstrike(oldTemplate)

		expected = ("{{Bracket|Bracket/2|id=TESTID\n" +
			"|R1M1header=Ola\n"
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

	def testValorantConvert(self):
		text = """
		{{2SETeamBracket
		|R1D1team=ROG Academy |R1D1score=1 |R1D1win=
		|R1D2team=S8ul Esports |R1D2score=2 |R1D2win=1
		|R1G1details={{BracketMatchSummary
		|date=November 27, 2021 - 20:30 {{Abbr/IST}} |finished=true
		|youtube=Skyesports
		|map1t1p1=BotCydex|map1t1a1=skye|map1t1kda1=9/18/10|map1t1acs1=77
		|map1t1p2=Equinox|map1t1a2=cypher|map1t1kda2=21/19/7|map1t1acs2=235
		|map1t1p3=LuDraa|map1t1a3=astra|map1t1kda3=21/16/10|map1t1acs3=230
		|map1t1p4=Kaizen|map1t1a4=jett|map1t1kda4=22/19/2|map1t1acs4=268
		|map1t1p5=wondRRRR|map1t1a5=sova|map1t1kda5=17/16/9|map1t1acs5=207

		|map1t2p1=BadmaN|map1t2a1=breach|map1t2kda1=13/17/11|map1t2acs1=172
		|map1t2p2=Binks|map1t2a2=killjoy|map1t2kda2=11/20/6|map1t2acs2=147
		|map1t2p3=Ezzy|map1t2a3=astra|map1t2kda3=17/18/9|map1t2acs3=181
		|map1t2p4=godvexy|map1t2a4=sova|map1t2kda4=15/17/11|map1t2acs4=189
		|map1t2p5=strixx|map1t2a5=jett|map1t2kda5=32/18/5|map1t2acs5=357

		|map1t1firstside=atk|map1t1atk=10|map1t1def=3|map1t2atk=9|map1t2def=2
		|map1=Haven|map1score=13-11|map1length=49:24|map1win=1|vodgame1=}}}}
		"""

		oldTemplate = mwparserfromhell.parse(text).filter_templates()[0]
		oldTemplate = Template(oldTemplate)
		oldTemplate.add('1', 'Bracket/2')
		oldTemplate.add('2', '2SETeamBracket')
		oldTemplate.add('id', 'TESTID')
		oldTemplate.add('type', 'team')

		bracket = BracketValorant(oldTemplate)

		expected = ("{{Bracket|Bracket/2|id=TESTID\n" +
            "\n" +
            "<!-- Grand Final -->\n" +
            "|R1M1={{Match\n" +
			"  |date=November 27, 2021 - 20:30 {{Abbr/IST}} |finished=true\n"
            "  |opponent1={{TeamOpponent|ROG Academy|score=1}}\n" +
            "  |opponent2={{TeamOpponent|S8ul Esports|score=2}}\n" +
            "  |winner=2\n" +
            "  |youtube=Skyesports\n" +
            "  |map1={{Map\n" +
            "    |t1p1={{PSI|player=BotCydex|agent=skye|kills=9|deaths=18|assists=10|acs=77}}\n" +
			"    |t1p2={{PSI|player=Equinox|agent=cypher|kills=21|deaths=19|assists=7|acs=235}}\n" +
			"    |t1p3={{PSI|player=LuDraa|agent=astra|kills=21|deaths=16|assists=10|acs=230}}\n" +
			"    |t1p4={{PSI|player=Kaizen|agent=jett|kills=22|deaths=19|assists=2|acs=268}}\n" +
			"    |t1p5={{PSI|player=wondRRRR|agent=sova|kills=17|deaths=16|assists=9|acs=207}}\n" +
			"\n" +
			"    |t2p1={{PSI|player=BadmaN|agent=breach|kills=13|deaths=17|assists=11|acs=172}}\n" +
			"    |t2p2={{PSI|player=Binks|agent=killjoy|kills=11|deaths=20|assists=6|acs=147}}\n" +
			"    |t2p3={{PSI|player=Ezzy|agent=astra|kills=17|deaths=18|assists=9|acs=181}}\n" +
			"    |t2p4={{PSI|player=godvexy|agent=sova|kills=15|deaths=17|assists=11|acs=189}}\n" +
			"    |t2p5={{PSI|player=strixx|agent=jett|kills=32|deaths=18|assists=5|acs=357}}\n" +
			"\n" +
			"    |t1firstside=atk|t1atk=10|t1def=3|t2atk=9|t2def=2\n" +
			"    |map=Haven|finished=true|length=49:24|winner=1\n"
			"  }}\n" +
			"}}\n}}"
		)

		self.assertEqual(expected, str(bracket))


	def testValidReset(self):
		fakeTemplate = Template.createFakeTemplate()
		fakeTemplate.add('winner', '1')
		fakeTemplate.add('nested', '{{foo|bar=1}}')
		fakeTemplate.add('ff', 'olas')

		match = Match([TeamOpponent('saw', '1'), TeamOpponent('ftw', '0')], fakeTemplate)

		isValidReset = BracketCounterstrike.isMatchValidResetOrThird

		#Non extra match are always "valid"
		self.assertEqual(True, isValidReset(match, False, 'R1M1'))
		self.assertEqual(True, isValidReset(match, False, THIRD_PLACE_MATCH))
		self.assertEqual(True, isValidReset(match, True, RESET_MATCH))

		#Reset match should be
		match.opponents[0].score = ''
		match.opponents[1].score = ''
		self.assertEqual(True, isValidReset(match, False, 'R1M1'))
		self.assertEqual(True, isValidReset(match, False, THIRD_PLACE_MATCH))
		self.assertEqual(True, isValidReset(match, True, RESET_MATCH))

		match.template.remove('nested')
		self.assertEqual(True, isValidReset(match, False, 'R1M1'))
		self.assertEqual(True, isValidReset(match, False, THIRD_PLACE_MATCH))
		self.assertEqual(True, isValidReset(match, True, RESET_MATCH))

		match.template.remove('winner')
		match.template.remove('ff')
		self.assertEqual(True, isValidReset(match, False, 'R1M1'))
		self.assertEqual(False, isValidReset(match, False, THIRD_PLACE_MATCH))
		self.assertEqual(False, isValidReset(match, True, RESET_MATCH))

		match.opponents[0].score = '1'
		self.assertEqual(True, isValidReset(match, True, RESET_MATCH))
