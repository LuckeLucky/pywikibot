import mwparserfromhell

from scripts.match2.commons.template import Template
from scripts.match2.commons.utils import importClass
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
		|hltv=2368518|vodgame1=testvod}}}}
		"""
		oldTemplate = mwparserfromhell.parse(text).filter_templates()[0]
		oldTemplate = Template.initFromTemplate(oldTemplate)
		oldTemplate.add('1', 'Bracket/2')
		oldTemplate.add('2', '2SETeamBracket')
		oldTemplate.add('id', 'TESTID')
		oldTemplate.add('type', 'team')

		csClass = importClass('counterstrike', 'Bracket')
		bracket = csClass(oldTemplate)

		expected = ("{{Bracket|Bracket/2|id=TESTID\n" +
			"|R1M1header=Ola\n"
			"\n" +
			"<!-- Grand Final -->\n" +
			"|R1M1={{Match\n" +
			"    |opponent1={{TeamOpponent|saw|score=1}}\n" +
			"    |opponent2={{TeamOpponent|ftw|score=2}}\n" +
			"    |date=December 20, 2023 - 11:00 {{Abbr/CEST}}|finished=true\n" +
			"    |winner=2\n" +
			"    |twitch=\n" +
			"    |hltv=2368518\n" +
			"    |map1={{Map|map=Overpass|finished=true\n" +
			"        |t1firstside=ct|t1t=11|t1ct=5|t2t=10|t2ct=0\n" +
			"        |stats=168110|vod=testvod\n" +
			"    }}\n" +
			"    |map2={{Map|map=Ancient|finished=true\n" +
			"        |t1firstside=t|t1t=2|t1ct=0|t2t=3|t2ct=13\n" +
			"        |stats=168105\n" +
			"    }}\n" +
			"    |map3={{Map|map=Vertigo|finished=true\n" +
			"        |t1firstside=t|t1t=14|t1ct=0|t2t=15|t2ct=1\n" +
			"        |stats=168136\n" +
			"    }}\n" +
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
		oldTemplate = Template.initFromTemplate(oldTemplate)
		oldTemplate.add('1', 'Bracket/2')
		oldTemplate.add('2', '2SETeamBracket')
		oldTemplate.add('id', 'TESTID')
		oldTemplate.add('type', 'team')

		valorantClass = importClass('valorant', 'Bracket')
		bracket = valorantClass(oldTemplate)

		expected = ("{{Bracket|Bracket/2|id=TESTID\n" +
			"\n" +
			"<!-- Grand Final -->\n" +
			"|R1M1={{Match\n" +
			"    |date=November 27, 2021 - 20:30 {{Abbr/IST}}|finished=true\n"
			"    |opponent1={{TeamOpponent|ROG Academy|score=1}}\n" +
			"    |opponent2={{TeamOpponent|S8ul Esports|score=2}}\n" +
			"    |winner=2\n" +
			"    |youtube=Skyesports\n" +
			"    |map1={{Map\n" +
			"        |t1p1={{PSI|player=BotCydex|agent=skye|kills=9|deaths=18|assists=10|acs=77}}\n" +
			"        |t1p2={{PSI|player=Equinox|agent=cypher|kills=21|deaths=19|assists=7|acs=235}}\n" +
			"        |t1p3={{PSI|player=LuDraa|agent=astra|kills=21|deaths=16|assists=10|acs=230}}\n" +
			"        |t1p4={{PSI|player=Kaizen|agent=jett|kills=22|deaths=19|assists=2|acs=268}}\n" +
			"        |t1p5={{PSI|player=wondRRRR|agent=sova|kills=17|deaths=16|assists=9|acs=207}}\n" +
			"\n" +
			"        |t2p1={{PSI|player=BadmaN|agent=breach|kills=13|deaths=17|assists=11|acs=172}}\n" +
			"        |t2p2={{PSI|player=Binks|agent=killjoy|kills=11|deaths=20|assists=6|acs=147}}\n" +
			"        |t2p3={{PSI|player=Ezzy|agent=astra|kills=17|deaths=18|assists=9|acs=181}}\n" +
			"        |t2p4={{PSI|player=godvexy|agent=sova|kills=15|deaths=17|assists=11|acs=189}}\n" +
			"        |t2p5={{PSI|player=strixx|agent=jett|kills=32|deaths=18|assists=5|acs=357}}\n" +
			"\n" +
			"        |t1firstside=atk|t1atk=10|t1def=3|t2atk=9|t2def=2\n" +
			"        |map=Haven|finished=true|length=49:24|winner=1\n"
			"    }}\n" +
			"}}\n}}"
		)

		self.assertEqual(expected, str(bracket))

	def testDota2Convert(self):
		text = """
			{{2SETeamBracket
			|R1D1team=vp |R1D1score=0 |R1D1win=
			|R1D2team=nigma |R1D2score=2 |R1D2win=1
			|R1G1details={{BracketMatchSummary
			|date=June 10, 2021 - 00:15 {{abbr/EEST}}
			|finished=true
			|twitch=WePlayDota|youtube=WePlay Dota
			|vodgame1=https://youtu.be/hYrVnZS4_kY?t=5457
			|matchid1=6034640592
			|match1={{Match
			|team1side=dire
			|t1h1=mars|t1h2=ancient apparition|t1h3=dark willow|t1h4=magnus|t1h5=ursa
			|t1b1=wisp|t1b2=dragon knight|t1b3=timbersaw|t1b4=dark seer|t1b5=phoenix|t1b6=terrorblade|t1b7=luna
			|team2side=radiant
			|t2h1=lion|t2h2=invoker|t2h3=rubick|t2h4=axe|t2h5=spectre
			|t2b1=templar assassin|t2b2=enchantress|t2b3=broodmother|t2b4=puck|t2b5=faceless void|t2b6=morphling|t2b7=phantom assassin
			|length=37m46s|win=2
			}}}}}}
		"""

		oldTemplate = mwparserfromhell.parse(text).filter_templates()[0]
		oldTemplate = Template.initFromTemplate(oldTemplate)
		oldTemplate.add('1', 'Bracket/2')
		oldTemplate.add('2', '2SETeamBracket')
		oldTemplate.add('id', 'TESTID')
		oldTemplate.add('type', 'team')

		dota2class = importClass('dota2', 'Bracket')
		bracket = dota2class(oldTemplate)

		expected = ("{{Bracket|Bracket/2|id=TESTID\n" +
			"\n" +
			"<!-- Grand Final -->\n" +
			"|R1M1={{Match2\n" +
			"|opponent1={{TeamOpponent|vp|score=0}}\n" +
			"|opponent2={{TeamOpponent|nigma|score=2}}\n" +
			"|date=June 10, 2021 - 00:15 {{abbr/EEST}}\n" +
			"|finished=true\n"
			"|winner=2\n" +
			"|twitch=WePlayDota\n"
			"|youtube=WePlay Dota\n"
			"|vodgame1=https://youtu.be/hYrVnZS4_kY?t=5457\n" +
			"|matchid1=6034640592\n" +
			"|map1={{Map\n" +
			"|team1side=dire\n" +
			"|t1h1=mars|t1h2=ancient apparition|t1h3=dark willow|t1h4=magnus|t1h5=ursa\n" +
			"|t1b1=wisp|t1b2=dragon knight|t1b3=timbersaw|t1b4=dark seer|t1b5=phoenix|t1b6=terrorblade|t1b7=luna\n" +
			"|team2side=radiant\n" +
			"|t2h1=lion|t2h2=invoker|t2h3=rubick|t2h4=axe|t2h5=spectre\n" +
			"|t2b1=templar assassin|t2b2=enchantress|t2b3=broodmother|t2b4=puck|t2b5=faceless void|t2b6=morphling|t2b7=phantom assassin\n" +
			"|length=37m46s|winner=2\n" +
			"}}\n" +
			"}}\n" +
			"}}"
		)

		self.assertEqual(expected, str(bracket))

	def testValidReset(self):
		fakeTemplate = Template.createFakeTemplate()
		fakeTemplate.add('winner', '1')
		fakeTemplate.add('nested', '{{foo|bar=1}}')
		fakeTemplate.add('ff', 'olas')

		match = Match([TeamOpponent(name = 'saw', score = '1'), TeamOpponent(name = 'ftw', score = '0')], fakeTemplate)

		csClass = importClass('counterstrike', 'Bracket')
		isValidReset = csClass.isMatchValidResetOrThird

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

	def testMapConversionStarcraftMatchMaps2v2(self):
		text = """
		{{MatchMaps/Legacy2v2
		|player1=Szinkler
		|player3=Xenoma
		|player2=Cuervin
		|player4=Shinovy
		|winner=1
		}}
		"""
		oldTemplate = mwparserfromhell.parse(text).filter_templates()[0]
		oldTemplate = Template.initFromTemplate(oldTemplate)
		mapClass = importClass('starcraft', 'Map')

		newMap = mapClass(1, oldTemplate)
		expected = '{{Map|map=|winner=1|t1p1=Szinkler|t1p2=Xenoma|t2p1=Cuervin|t2p2=Shinovy}}'
		self.assertEqual(expected, str(newMap))

	def testMapConversionStarcraftMatchMaps(self):
		text = """
		{{MatchMaps/Legacy
		|player1=Szinkler
		|player2=Cuervin
		|winner=1
		}}
		"""

		oldTemplate = mwparserfromhell.parse(text).filter_templates()[0]
		oldTemplate = Template.initFromTemplate(oldTemplate)
		mapClass = importClass('starcraft', 'Map')

		newMap = mapClass(1, oldTemplate)
		expected = '{{Map|map=|winner=1|t1p1=Szinkler|t2p1=Cuervin}}'
		self.assertEqual(expected, str(newMap))
		
	def testProLeague(self):
		text = """
		{{ProleagueMatch
		|m1p1=Szinkler
		|m1p2=Cuervin
		|m1win=1
		}}
		"""

		oldTemplate = mwparserfromhell.parse(text).filter_templates()[0]
		oldTemplate = Template.initFromTemplate(oldTemplate)
		mapClass = importClass('starcraft', 'Map')
		newMap = mapClass(1, oldTemplate)
		newMap.prefix = 'm1'
		expected = '{{Map|map=|winner=1|t1p1=Szinkler|t2p1=Cuervin}}'
		self.assertEqual(expected, str(newMap))

	def testProLeague2v2(self):
		text = """
		{{Proleague04-05Match
		|m1p1=Szinkler
		|m1p3=Cuervin
		|m1win=1
		}}
		"""

		oldTemplate = mwparserfromhell.parse(text).filter_templates()[0]
		oldTemplate = Template.initFromTemplate(oldTemplate)
		mapClass = importClass('starcraft', 'Map')
		newMap = mapClass(1, oldTemplate)
		newMap.prefix = 'm1'
		expected = '{{Map|map=|winner=1|t1p1=Szinkler|t2p1=Cuervin}}'
		self.assertEqual(expected, str(newMap))

	def testHearthStoneTeamMatch(self):
		text = """
		{{TeamMatchBo3
		|team1=dogehouse
		|team2=mym
		|teamwin=2
		|date=May 7, 2014 18:00 {{Abbr/CEST}}
		|lrthread=
		|vod1=https://www.twitch.tv/taketvred/c/4252056
		|vod2=https://www.twitch.tv/taketvred/c/4252076
		|vod3=https://www.twitch.tv/taketvred/c/4252083
		|vod4=https://www.twitch.tv/taketvred/c/4252098
		|collapsed=
		|finished=true

		<!-- Match 1 -->
		|m1p1=Artosis |m1p1flag=us |m1p1score=0
		|m1p2=Kunzi |m1p2flag=de |m1p2score=2
		|m1p1class1=Druid |m1p2class1=Warrior |m1win1=2
		|m1p1class2=Warlock |m1p2class2=Warrior |m1win2=2

		<!-- Match 2 -->
		|m2p1=StrifeCro |m2p1flag=us |m2p1score=0
		|m2p2=ThijsNL |m2p2flag=nl |m2p2score=2
		|m2p1class1=Warrior |m2p2class1=Druid |m2win1=2
		|m2p1class2=Druid |m2p2class2=Druid |m2win2=2

		<!-- Match 4 -->
		|m3p1=Ek0p |m3p1flag=de |m3p1score=2
		|m3p2=Ignite |m3p2flag=pt |m3p2score=1

		<!-- Match 5 -->
		|acep1=Ek0p |acep1flag=de |acep1score=1
		|acep2=ThijsNL |acep2flag=nl |acep2score=2
		|acep1class1=Druid |acep2class1=Druid |acewin1=2
		|acep1class2=Shaman |acep2class2=Druid |acewin2=1
		|acep1class3=Shaman |acep2class3=Hunter |acewin3=2
		}}
		"""

		oldTemplate = mwparserfromhell.parse(text).filter_templates()[0]
		oldTemplate = Template.initFromTemplate(oldTemplate, removeComments=True)
		oldTemplate.add('winner', '2')
		matchClass = importClass('hearthstone', 'Match')
		newMatch = matchClass([TeamOpponent(name = 'dogehouse'),
					TeamOpponent(name = 'mym')], oldTemplate)
		expected = ("{{Match\n" +
			"    |date=May 7, 2014 18:00 {{Abbr/CEST}}|finished=true\n" +
			"    |lrthread=\n" +
			"    |vod=\n" +
			"    |opponent1={{TeamOpponent|dogehouse|score=1}}\n" +
			"    |opponent2={{TeamOpponent|mym|score=3}}\n" +
			"    |map1={{Map|subgroup=1|o1p1=Artosis|o1c1=Druid|o2p1=Kunzi|o2c1=Warrior|winner=2|vod=https://www.twitch.tv/taketvred/c/4252056}}\n" +
			"    |map2={{Map|subgroup=1|o1p1=Artosis|o1c1=Warlock|o2p1=Kunzi|o2c1=Warrior|winner=2|vod=https://www.twitch.tv/taketvred/c/4252056}}\n" +
			"    |map3={{Map|subgroup=2|o1p1=StrifeCro|o1c1=Warrior|o2p1=ThijsNL|o2c1=Druid|winner=2|vod=https://www.twitch.tv/taketvred/c/4252076}}\n" +
			"    |map4={{Map|subgroup=2|o1p1=StrifeCro|o1c1=Druid|o2p1=ThijsNL|o2c1=Druid|winner=2|vod=https://www.twitch.tv/taketvred/c/4252076}}\n" +
			"    |map5={{Map|map=Submatch 3|o1p1=Ek0p|o2p1=Ignite|score1=2|score2=1|winner=1|vod=https://www.twitch.tv/taketvred/c/4252083}}\n" +
			"    |submatch4header=Ace Match\n" +
			"    |map6={{Map|subgroup=4|o1p1=Ek0p|o1c1=Druid|o2p1=ThijsNL|o2c1=Druid|winner=2|vod=https://www.twitch.tv/taketvred/c/4252098}}\n" +
			"    |map7={{Map|subgroup=4|o1p1=Ek0p|o1c1=Shaman|o2p1=ThijsNL|o2c1=Druid|winner=1|vod=https://www.twitch.tv/taketvred/c/4252098}}\n" +
			"    |map8={{Map|subgroup=4|o1p1=Ek0p|o1c1=Shaman|o2p1=ThijsNL|o2c1=Hunter|winner=2|vod=https://www.twitch.tv/taketvred/c/4252098}}\n" +
			"}}"
		)

		self.assertEqual(expected, str(newMatch))




