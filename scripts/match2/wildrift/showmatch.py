from ..commons.singlematch import Singlematch as commonsSinglematch
from .match import Match

class Singlematch(commonsSinglematch):
	Match = Match
