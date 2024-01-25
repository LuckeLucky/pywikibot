import mwparserfromhell
from tests.aspects import TestCase

from scripts.table_to_points_table import processTable

class PointsTableTest(TestCase):
	net = False
	maxDiff = None
	def testConversion(self):
		text ="""
			{|class="wikitable sortable" class="table table-bordered prizepooltable" style="text-align:center;" data-cutafter="10"
			|+ style="text-align:center"|Top 8
			|-
			!#
			!Team
			![[Volcano League/2020/Closing/Tournament_1|#1]]
			![[Volcano League/2020/Closing/Tournament_2|#2]]
			![[Volcano League/2020/Closing/Tournament_3|#3]]
			![[Volcano League/2020/Closing/Tournament_4|#4]]
			!Σ
			|- style="background-color:rgb(204,255,204)"
			|'''1'''|| align="left" |{{Team|geekside esports}}
			|1100||1050||2200||5500||'''9850'''
			|-
			|- style="background-color:rgb(204,255,204)"
			|'''2'''|| align="left" |{{Team|descuydado esports}}
			|700||1650||4400||2750||'''9500'''
			|-
			|- style="background-color:rgb(204,255,204)"
			|'''3'''|| align="left" |{{Team|raven gaming}}
			|100||1650||3200||2750||'''7700'''
			|-
			|- style="background-color:rgb(204,255,204)"
			|'''4'''|| align="left" |{{Team|skull cracker}}
			|2200||3300||400||1750||'''7650'''
			|-
			|'''5'''|| align="left" |{{Team|black condors esports}}
			|400||600||1400||4000||'''6400'''
			|-
			|'''6'''|| align="left" |{{Team|hooked esports}}
			|700||2400||1400||1750||'''6250'''
			|-
			|'''7'''|| align="left" |{{Team|volta7 cebci}}
			|1100||1050||1400||1750||'''5300'''
			|-
			|'''8'''|| align="left" |{{Team|predator esports ecuador}}
			|400||0||2200||1750||'''4350'''
			|-
			|}
		"""

		wikicode = mwparserfromhell.parse(text)
		table = wikicode.filter_tags(matches=lambda node: node.tag == "table")[0]
		new = processTable(str(table))
		
		expected = ("{{Points start|event1=#1|event1link=Volcano League/2020/Closing/Tournament_1|event2=#2|event2link=Volcano League/2020/Closing/Tournament_2|event3=#3|event3link=Volcano League/2020/Closing/Tournament_3|event4=#4|event4link=Volcano League/2020/Closing/Tournament_4}}\n"+
			"{{Points slot|geekside esports|place=1|points1=1100|points2=1050|points3=2200|points4=5500|total=9850}}\n"+
			"{{Points slot|descuydado esports|place=2|points1=700|points2=1650|points3=4400|points4=2750|total=9500}}\n"+
			"{{Points slot|raven gaming|place=3|points1=100|points2=1650|points3=3200|points4=2750|total=7700}}\n"+
			"{{Points slot|skull cracker|place=4|points1=2200|points2=3300|points3=400|points4=1750|total=7650}}\n"+
			"{{Points slot|black condors esports|place=5|points1=400|points2=600|points3=1400|points4=4000|total=6400}}\n"+
			"{{Points slot|hooked esports|place=6|points1=700|points2=2400|points3=1400|points4=1750|total=6250}}\n"+
			"{{Points slot|volta7 cebci|place=7|points1=1100|points2=1050|points3=1400|points4=1750|total=5300}}\n"+
			"{{Points slot|predator esports ecuador|place=8|points1=400|points2=0|points3=2200|points4=1750|total=4350}}\n"+
			"{{Points end}}\n")

		self.assertEqual(expected, new)
