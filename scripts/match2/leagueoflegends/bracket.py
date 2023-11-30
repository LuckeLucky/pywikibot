from mwparserfromhell.nodes import Template
from ..bracket import Bracket as Base
from .match import Match

class BracketLeagueOfLegends(Base):
    def __init__(self, oldTemplateName: str, bracket: Template) -> None:
        super().__init__(oldTemplateName, bracket)

    def match_class(self):
        return Match