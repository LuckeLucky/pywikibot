import io
from mwparserfromhell.nodes import Template
from scripts.match2.utils import Template

from ..utils import *
from ..match import Match
from ..opponent import Opponent

from .map import Map

STREAMS = [
	'stream',
	'twitch',
	'twitch2',
	'afreeca',
	'afreecatv',
	'dailymotion',
	'douyu',
	'huomao',
	'youtube',
	'facebook',
	'pandatv',
	'huya',
	'bilibili',
	'steamtv',
	'vod',
	'vod2',
	'reddit'
]

class Match(Match):
	def get_maps(self):
		for key in PrefixIterator('match', self.data):
			match_template = get_parameter_template(self.template, key)
			index = key.replace('match', '')
			#Winner outside of MatchLua
			winner = get_value_or_empty(self.data, 'map' + index + 'winner')
			if match_template is None and winner:
				match_template = Template('MatchLua')
				match_template.add('win', winner)
			elif not get_parameter_str(match_template, 'win') and winner:
				match_template.add('win', winner)

			self.maps.append(Map(int(index), match_template))
